
from gi.repository import GObject
from pywebp.helpers import get_boolean, get_float, get_int


class Setting(object):
    """Stores a setting and its attributes.

    This class should not be used directly. Instead it is used as BaseClass for
    different types of settings.

    Attributes:
        name: Name of the setting as string.

        _datatype: Python type of the setting.
        _default_value: Default value of the setting stored in its python type.
        _value: Value of the setting stored in its python type.
    """

    def __init__(self, name, default_value):
        """Initialize attributes with default values.

        Args:
            name: Name of the setting to initialize.
            default_value: Default value of the setting to start with.
        """
        self.name = name
        self._default_value = default_value
        self._value = default_value
        self._n = 0

    def get_default(self):
        return self._default_value

    def get_value(self):
        return self._value

    def is_default(self):
        return self._value == self._default_value

    def set_to_default(self):
        self._value = self._default_value


class BoolSetting(Setting):
    """Stores a boolean setting."""

    def override(self, new_value):
        self._value = get_boolean(new_value)

    def toggle(self):
        self._value = not self._value


class IntSetting(Setting):
    """Stores an integer setting."""

    def override(self, new_value):
        self._value = get_int(new_value)

    def add(self, value, multiplier):
        """Add a value to the currently stored integer.

        Args:
            value: The integer value to add.
            multiplier: Integer to multiply value with.
        """
        value = get_int(value, allow_sign=True)
        multiplier = get_int(multiplier, allow_sign=False)
        self._value += value * multiplier


class FloatSetting(Setting):
    """Stores a float setting."""

    def override(self, new_value):
        self._value = get_float(new_value)

    def add(self, value, multiplier):
        """Add a value to the currently stored float.

        Args:
            value: The float value to add.
            multiplier: Float to multiply value with.
        """
        value = get_float(value, allow_sign=True)
        multiplier = get_float(multiplier, allow_sign=False)
        self._value += value * multiplier


class ThumbSizeSetting(Setting):
    """Stores a thumbnail size setting.

    This setting is stored as a python tuple with two equal integer values. The
    integer value must be one of 64, 128, 256, 512.
    """

    def override(self, new_value):
        """Override the setting with a new thumbnail size.

        Args:
            new_value: String in the form of "(val, val)" for the new value.
        """
        new_value = new_value.lstrip("(").rstrip(")")
        int_tuple = new_value.split(",")
        if len(int_tuple) != 2:
            error = "Tuple must be of the form (val, val)"
            raise ValueError(error)
        int_tuple = (get_int(int_tuple[0]), get_int(int_tuple[1]))
        if int_tuple[0] != int_tuple[1]:
            error = "Thumbnail width and height must be equal"
            raise ValueError(error)
        if int_tuple[0] not in [64, 128, 256, 512]:
            error = "Thumbnail size must be one of 64, 128, 256 and 512"
            raise ValueError(error)
        self._value = tuple(int_tuple)


class GeometrySetting(Setting):
    """Stores a geometry setting.

    This setting is stored as python tuple of the form (width, height) and can
    be set from a string in the form "WIDTHxHEIGHT".
    """

    def override(self, new_value):
        """Override the setting with a new geometry.

        Args:
            new_value: String in the form of "WIDTHxHEIGHT" for the new value.
        """
        geometry = new_value.split("x")
        if len(geometry) != 2:
            error = "Geometry must be of the form WIDTHxHEIGHT"
            raise ValueError(error)
        self._value = (get_int(geometry[0]), get_int(geometry[1]))


class SettingStorage(GObject.Object):
    """Stores all settings for vimiv.

    Settings can be accessed via SettingStorage["setting_name"] and changed by
    calling SettingStorage.override("setting_name", new_value).

    Attributes:
        _aliases: Dictionary containing all aliases.
        _settings: List of all Setting objects. Should not be accessed directly.
        _n: Integer for iterator.

    Signals:
        changed: Emitted when a setting was changed.
    """

    def __init__(self):
        super(SettingStorage, self).__init__()
        self._aliases = {}
        self._settings = [
            BoolSetting("darkmode", True),
            ThumbSizeSetting("default_thumbsize", (128, 128)),
            GeometrySetting("geometry", (800, 400))
        ]
        self._n = 0

    def override(self, name, new_value=None):
        """Override a setting in the storage.

        Args:
            name: Name of the setting to override.
            new_value: Value to override the setting with. If None use default.
        """
        setting = self[name]
        if new_value is None:
            setting.set_to_default()
        else:
            setting.override(new_value)
        self.emit("changed", name)

    def toggle(self, name):
        """Toggle a setting in the storage.

        If the setting is not a boolean, an exception is raised.

        Args:
            name: Name of the setting to toggle.
        """
        if isinstance(self[name], BoolSetting):
            self[name].toggle()
            self.emit("changed", name)
        else:
            error = "Cannot toggle non boolean setting '%s'" % (name)
            raise Exception(error)

    def add_to(self, name, value, multiplier):
        """Add a number to a setting in the storage.

        If the setting is not a number, an exception is raised.

        Args:
            name: Name of the setting to change.
            value: Value to add.
            multiplier: Multiply value by this. Used for num_str.
        """
        if isinstance(self[name], (IntSetting, FloatSetting)):
            self[name].add(value, multiplier)
            self.emit("changed", name)
        else:
            error = "Cannot add to non number setting '%s'" % (name)
            raise Exception(error)

    def reset(self):
        """Reset all settings to their default value."""
        for setting in self:
            setting.set_to_default()

    def __getitem__(self, name):
        """Receive a setting via its name."""
        for setting in self._settings:
            if setting.name == name:
                return setting
        raise Exception("No setting called '%s'" % (name))

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        """Iterate over settings."""
        if (self._n - 1) < len(self._settings) - 1:
            self._n += 1
            return self._settings[self._n - 1]
        else:
            raise StopIteration


# Initiate signals for the SettingsStorage
GObject.signal_new("changed", SettingStorage, GObject.SIGNAL_RUN_LAST,
                   None, (GObject.TYPE_PYOBJECT,))


# Initialize an actual SettingsStorage object to work with
settings = SettingStorage()
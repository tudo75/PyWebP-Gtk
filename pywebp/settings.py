#
#  MIT License
#
#  Copyright (c) 2019-2020 Nicola Tudino aka tudo75
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#

import os

from gi.repository import GObject, GLib
from pywebp.helpers import error_message

DATA_DIR = os.path.join(GLib.get_user_data_dir(), 'pywebp_gtk')
CONFIG_FILE = os.path.join(DATA_DIR, 'pywebp_gtk.ini')
SETTINGS_GROUP_NAME = "Settings"
COPYRIGHT = """

MIT License

Copyright (c) 2019-2021 Nicola Tudino aka tudo75

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


class SettingStorage(GObject.Object):
    """Stores all settings.

    Settings can be accessed via SettingStorage.get_type("key") and changed by
    calling SettingStorage.set_type("key", value), where type is the type of data(boolean,integer,etc).

    Signals:
        changed: Emitted when a setting was changed.
    """

    def __init__(self):
        super(SettingStorage, self).__init__()
        self._init_from_keyfile()

    @staticmethod
    def _init_from_keyfile():
        """Initialize te key file in DATA_DIR folder with CONFIG_FILE path and create default values for keys
        """
        _keyfile = GLib.KeyFile()
        # check if DATA_DIR exist and eventually create it
        if not os.path.exists(DATA_DIR):
            try:
                os.makedirs(DATA_DIR)
            except OSError as error:
                print(error)
                print("Creation of the directory %s failed" % DATA_DIR)
            else:
                print("Successfully created the directory %s " % DATA_DIR)

        # check if CONFIG_FILE exist and eventually create it
        if os.path.exists(CONFIG_FILE):
            _keyfile.load_from_file(CONFIG_FILE, GLib.KeyFileFlags.KEEP_COMMENTS)
            print("CONFIG_FILE loaded")
        else:
            _keyfile = GLib.KeyFile.new()
            _keyfile.set_comment(None, None, COPYRIGHT)
            print("no CONFIG_FILE, new keyfile created")

        # check if SETTINGS_GROUP_NAME settings group exist and eventually create and initialize it
        if not _keyfile.has_group(SETTINGS_GROUP_NAME):
            _keyfile.set_boolean(SETTINGS_GROUP_NAME, "darkmode", True)
            _keyfile.set_integer_list(SETTINGS_GROUP_NAME, "default_thumbsize", [128, 128])
            _keyfile.set_integer_list(SETTINGS_GROUP_NAME, "geometry", [800, 400])

        _keyfile.save_to_file(CONFIG_FILE)

    @staticmethod
    def _get_keyfile():
        """Load keyfile from CONFIG_FILE

        Returns:
            keyfile containing settings
        """
        _keyfile = GLib.KeyFile()
        try:
            _keyfile.load_from_file(CONFIG_FILE, GLib.KeyFileFlags.KEEP_COMMENTS)
        except GLib.Error as error:
            error_message(error)
        finally:
            return _keyfile

    def get_boolean(self, key) -> bool:
        """Return boolean value of the key setting

        Args:
            key: the name of the setting containing the boolean value to be retrieved

        Returns:
            the value associated with the key as a boolean, or False if the key was not found or could not be parsed.
        """
        keyfile = self._get_keyfile()
        try:
            result = keyfile.get_boolean(SETTINGS_GROUP_NAME, key)
        except GLib.Error as error:
            error_message(error.message)
            result = False

        return result

    def set_boolean(self, key, value):
        """ Associates a new boolean value with key. If key cannot be found then it is created.

        Args:
            key: key name
            value: True or False

        Return:
            True if value is set, False otherwise
        """
        keyfile = self._get_keyfile()
        result = False
        if isinstance(value, bool):
            try:
                keyfile.set_boolean(SETTINGS_GROUP_NAME, key, value)
                keyfile.save_to_file(CONFIG_FILE)
            except GLib.Error as error:
                error_message(error.message)
            finally:
                result = True

        return result

    def get_integer(self, key) -> int:
        """Return integer value of the key setting

        Args:
            key: the name of the setting containing the integer value to be retrieved

        Returns:
            the value associated with the key as an integer, or 0 if the key was not found or could not be parsed.
        """
        keyfile = self._get_keyfile()
        try:
            result = keyfile.get_integer(SETTINGS_GROUP_NAME, key)
        except GLib.Error as error:
            error_message(error.message)
            result = 0

        return result

    def set_integer(self, key, value):
        """ Associates a new integer value with key. If key cannot be found then it is created.

        Args:
            key: key name
            value: an integer value

        Return:
            True if value is set, False otherwise
        """
        keyfile = self._get_keyfile()
        result = False
        if isinstance(value, int):
            try:
                keyfile.set_integer(SETTINGS_GROUP_NAME, key, value)
                keyfile.save_to_file(CONFIG_FILE)
            except GLib.Error as error:
                error_message(error.message)
            finally:
                result = True

        return result

    def get_integer_list(self, key) -> [int]:
        """Return a list of integer values of the key setting

        Args:
            key: the name of the setting containing the list of integer values to be retrieved

        Returns:
            the values associated with the key as a list of integers, or an empty list [] if the key was not found or
            could not be parsed. The returned list of integers should be freed with GLib.free() when no longer needed.
        """
        keyfile = self._get_keyfile()
        try:
            result = keyfile.get_integer_list(SETTINGS_GROUP_NAME, key)
        except GLib.Error as error:
            error_message(error.message)
            result = [0]

        return result

    def set_integer_list(self, key, my_list):
        """ Associates a list of integer values with key. If key cannot be found then it is created.

        Args:
            key: key name
            my_list: an array of integer values

        Return:
            True if value is set, False otherwise
        """
        keyfile = self._get_keyfile()
        result = False
        if all(isinstance(item, int) for item in my_list):
            try:
                keyfile.set_integer_list(SETTINGS_GROUP_NAME, key, my_list)
                keyfile.save_to_file(CONFIG_FILE)
            except GLib.Error as error:
                error_message(error.message)
            finally:
                result = True

        return result


# Initiate signals for the SettingsStorage
GObject.signal_new("changed", SettingStorage, GObject.SIGNAL_RUN_LAST,
                   None, (GObject.TYPE_PYOBJECT,))


# Initialize an actual SettingsStorage object to work with
settings = SettingStorage()

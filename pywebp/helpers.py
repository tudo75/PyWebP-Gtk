
import os

from gi.repository import Gtk

def sizeof_fmt(num) -> str:
    """Print size of a byte number in human-readable format.

    Args:
        num: File size in bytes.

    Return:
        str: File size in human-readable format.
    """
    for unit in ["B", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            if abs(num) < 100:
                return "%3.1f%s" % (num, unit)
            return "%3.0f%s" % (num, unit)
        num /= 1024.0
    return "%.1f%s" % (num, "Y")


def error_message(message, running_tests=False):
    """Show a GTK Error Pop Up with message.

    Args:
        message: The message to display.
        running_tests: If True running from testsuite. Do not show popup.
    """
    # Always print the error message first
    print("\033[91mError:\033[0m", message)
    # Then display a Gtk Popup
    popup = Gtk.Dialog(title="PyWEbP-GTK - Error", transient_for=Gtk.Window())
    popup.set_default_size(600, 1)
    popup.add_button(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)

    h_bar = Gtk.HeaderBar()
    h_bar.set_title("PyWEbP-GTK - Error")
    h_bar.set_show_close_button(True)
    popup.set_titlebar(h_bar)

    message_label = Gtk.Label()
    # Set up label so it actually follows the default width of 600
    message_label.set_hexpand(True)
    message_label.set_line_wrap(True)
    message_label.set_size_request(600, 1)
    message_label.set_text(message)
    box = popup.get_child()
    box.set_border_width(12)
    grid = Gtk.Grid()
    grid.set_column_spacing(12)
    box.pack_start(grid, False, False, 0)
    error_icon_path = os.path.join(os.path.dirname(__file__), 'images/icons/dialog-error/32.png')
    error_icon = Gtk.Image.new_from_file(error_icon_path)
    grid.attach(error_icon, 0, 0, 1, 1)
    grid.attach(message_label, 1, 0, 1, 1)
    popup.show_all()
    if not running_tests:
        popup.run()
        popup.destroy()

def get_boolean(value) -> bool:
    """Convert a value to a boolean.

    Args:
        value: String value to convert.
    Return:
        bool: True if string.lower() in ["yes", "true"]. False otherwise.
    """
    bool_val = False
    try:
        if value.lower() in ["yes", "true"]:
            bool_val = True
    except AttributeError:
        error = "Could not convert '%s' to bool, must be a string" % (value)
        raise AttributeError(error)
    return bool_val

def get_int(value, allow_sign=False) -> int:
    """Convert a value to an integer.

    Args:
        value: String value to convert.
        allow_sign: If True, negative values are allowed.
    Return:
        int(value) if possible.
    """
    try:
        # rstrip needed when 0. is passed via [count]
        int_val = int(value.rstrip("."))
    except ValueError:
        error = "Could not convert '%s' to int" % (value)
        raise ValueError(error)
    if int_val < 0 and not allow_sign:
        raise ValueError("Negative numbers are not supported.")
    return int_val


def get_float(value, allow_sign=False) -> float:
    """Convert a value to a float.

    Args:
        value: String value to convert.
        allow_sign: If True, negative values are allowed.
    Return:
        float(value) if possible.
    """
    try:
        float_val = float(value)
    except ValueError:
        error = "Could not convert '%s' to float" % (value)
        raise ValueError(error)
    if float_val < 0 and not allow_sign:
        raise ValueError("Negative numbers are not supported.")
    return float_val


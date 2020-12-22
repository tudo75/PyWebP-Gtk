
import sys

__license__ = "MIT"
__version__ = "0.0.1.dev0"
__author__ = __maintainer__ = "Nicola Tudino"
__email__ = "tudo75@gmail.com"

try:
    from gi import require_version
    require_version("Gtk", "3.0")
    require_version("Gdk", "3.0")
    from gi.repository import Gtk, GdkPixbuf, Gio, Gdk

except ImportError as import_error:
    message = import_error.msg + "\n" + "Are all dependencies installed?"
    print(message)
    sys.exit(1)
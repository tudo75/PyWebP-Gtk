#
#  MIT License
#
#  Copyright (c) 2020-2021 Nicola Tudino aka tudo75
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

import sys

__license__ = "MIT"
__version__ = "0.0.1.dev0"
__author__ = __maintainer__ = "Nicola Tudino"
__email__ = "tudo75@gmail.com"

try:
    from gi import require_version
    require_version("Gtk", "3.0")
    require_version("Gdk", "3.0")
    from gi.repository import Gtk, GdkPixbuf, Gio, Gdk, GLib

except ImportError as import_error:
    message = import_error.msg + "\n" + "Are all dependencies installed?"
    print(message)
    sys.exit(1)
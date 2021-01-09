#
#  MIT License
#
#  Copyright (c) 2019-2021 Nicola Tudino aka tudo75
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
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from pywebp.helpers import sizeof_fmt
from pywebp.settings import settings


class IconStore(Gtk.ListStore):
    """

    model schema:
    [
        str: img description,
        Pixbuf: image,
        str: full file path,
        str: file basename,
        str: file size
    ]
    """

    def __init__(self):
        super(IconStore, self).__init__()
        self.set_column_types([str, Pixbuf, str, str, str])

    def get_model(self) -> Gtk.ListStore:
        """Get model associated to the widget

        Returns:
            the model associated to the PyWebP.IconView widget
        """
        return self

    def add_to_model(self, filepath):
        """Add an image to the model associated to the PyWebP.IconView

        Args:
            filepath: full file path of the image

        """
        if not self.is_duplicate(filepath, 2):
            _basename = os.path.basename(filepath)
            _filesize = sizeof_fmt(os.path.getsize(filepath))
            self.append([_basename + "\nSize: " + _filesize,
                         Pixbuf.new_from_file_at_scale(filepath,
                                                       settings.get_integer_list("default_thumbsize")[0],
                                                       settings.get_integer_list("default_thumbsize")[1],
                                                       True),
                         filepath,
                         _basename,
                         _filesize])

    def remove_selected(self, items) -> bool:
        """Remove selected items from the thumbs panel

        Args:
            items:

        Returns:
            True if all selected items are removed, False otherwise
        """
        removed = True
        for item in items:
            if not self.remove(self.get_iter(item)):
                removed = False

        return removed

    def is_duplicate(self, value, column=2) -> bool:
        """

        Args:
            value: value to be verified in assigned column
            column: column containing the value to verify, default is 3 (full file path)

        Returns:
            True if value is present in model, False otherwise
        """
        _is_duplicate = False
        for row in self:
            if row[column] == value:
                _is_duplicate = True
                break
        return _is_duplicate

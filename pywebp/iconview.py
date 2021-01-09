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
from pywebp.iconstore import IconStore
from pywebp.settings import settings


class IconView(Gtk.IconView):


    def __init__(self, app):
        super(IconView, self).__init__()
        self._app = app
        self._init_gui()

    def _init_gui(self):
        self._model = IconStore()
        self.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.set_vexpand(True)
        self.set_text_column(0)
        self.set_pixbuf_column(1)
        self.set_tooltip_column(0)
        self.set_item_width(settings.get_integer_list("default_thumbsize")[0])
        self.set_item_padding(3)
        self.set_margin(3)
        self.set_column_spacing(3)
        self.set_model(self._model)
        self.connect("selection-changed", self._selection_changed)

    def _selection_changed(self, action):
        """

        Args:
            action:

        Returns:

        """
        selected = self.get_selected_items()
        if len(selected) == len(self._model):
            self._app.toolbar.set_select_all(True)
        else:
            self._app.toolbar.set_select_all(False)

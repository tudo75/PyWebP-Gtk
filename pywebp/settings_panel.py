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

from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk
from pywebp.settings import settings


class SettingsPanel(Gtk.Notebook):
    def __init__(self):
        super(SettingsPanel, self).__init__()
        self.init_panel()

    def init_panel(self):
        # self.set_scrollable(True)
        self.popup_enable()

        general_grid = Gtk.Grid()
        general_grid.set_border_width(8)
        general_grid.set_column_spacing(10)
        general_grid.attach(Gtk.Label("Enable dark mode"), 0, 0, 1, 1)
        darkmode_btn = Gtk.Switch()
        darkmode_btn.set_active(settings.get_boolean("darkmode"))
        general_grid.attach(darkmode_btn, 1, 0, 1, 1)

        cwebp_grid = Gtk.Grid()
        cwebp_grid.set_border_width(8)
        cwebp_grid.set_column_spacing(10)
        cwebp_grid.attach(Gtk.Label("Enable dark mode"), 0, 0, 1, 1)

        dwebp_grid = Gtk.Grid()
        dwebp_grid.set_border_width(8)
        dwebp_grid.set_column_spacing(10)
        dwebp_grid.attach(Gtk.Label("Enable dark mode"), 0, 0, 1, 1)

        self.append_page(general_grid, Gtk.Label('General'))
        self.append_page(cwebp_grid, Gtk.Label('cwebp'))
        self.append_page(dwebp_grid, Gtk.Label('dwebp'))

        self.show_all()


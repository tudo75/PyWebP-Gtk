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

from gi.repository import Gtk, GObject
from pywebp.settings import settings
from pywebp.helpers import error_message

COLUMN_SPACING = 30
ROW_SPACING = 30
BORDER_WIDTH = 8

class SettingsPanel(Gtk.Notebook):
    """SettingsPanel class for PyWebP.

    Inherits from Gtk.Notebook and includes all actions that apply to it.

    Attributes:
        _app: The main pywebp class to interact with.
    """

    def __init__(self, app):
        super(SettingsPanel, self).__init__()
        self._app = app
        self.init_panel()

    def init_panel(self):
        # self.set_scrollable(True)
        self.popup_enable()

        general_grid = Gtk.Grid()
        general_grid.set_border_width(BORDER_WIDTH)
        general_grid.set_column_spacing(COLUMN_SPACING)
        general_grid.set_row_spacing(ROW_SPACING)
        general_grid.set_column_homogeneous(True)
        general_grid.set_row_homogeneous(True)
        general_grid.attach(Gtk.Label("Enable dark mode"), 0, 0, 1, 1)
        darkmode_btn = Gtk.Switch()
        darkmode_btn.props.halign = Gtk.Align.CENTER
        # darkmode_btn.set_size_request(50, 20)
        darkmode_btn.set_active(settings.get_boolean("darkmode"))
        darkmode_btn.connect('state-set', self.toggle_darkmode)
        general_grid.attach(darkmode_btn, 1, 0, 1, 1)

        general_grid.attach(Gtk.Label("Enable"), 0, 1, 1, 1)
        general_grid.attach(Gtk.Label("Enable"), 1, 1, 1, 1)
        general_grid.attach(Gtk.Label("Enable"), 0, 2, 1, 1)
        general_grid.attach(Gtk.Label("Enable"), 1, 2, 1, 1)


        cwebp_grid = Gtk.Grid()
        cwebp_grid.set_border_width(BORDER_WIDTH)
        cwebp_grid.set_column_spacing(COLUMN_SPACING)
        cwebp_grid.set_row_spacing(ROW_SPACING)
        cwebp_grid.attach(Gtk.Label("Enable dark mode"), 0, 0, 1, 1)

        dwebp_grid = Gtk.Grid()
        dwebp_grid.set_border_width(BORDER_WIDTH)
        dwebp_grid.set_column_spacing(COLUMN_SPACING)
        dwebp_grid.set_row_spacing(ROW_SPACING)
        dwebp_grid.attach(Gtk.Label("Enable dark mode"), 0, 0, 1, 1)

        self.append_page(general_grid, Gtk.Label('General'))
        self.append_page(cwebp_grid, Gtk.Label('cwebp'))
        self.append_page(dwebp_grid, Gtk.Label('dwebp'))

        self.show_all()

    def toggle_darkmode(self, action, darkmode):
        """Want to enable dark mode theme or not

        Args:
            action: object connected to this fallback
            darkmode: True or False if app must use dark mode theme
        """
        print(action)
        print(darkmode)
        self._app.toggle_darkmode(darkmode)
        context_id = self._app.statusbar.get_context_id("message from switch")
        message = "Dark mode enabled"
        if not darkmode:
            message = "Dark mode disabled"
        self._app.push_status_message(message, context_id, 4)
        # error_message('switch clicked')





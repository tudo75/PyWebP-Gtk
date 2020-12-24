
from gi.repository import Gtk


class SettingsPanel(Gtk.Notebook):
    def __init__(self):
        super(SettingsPanel, self).__init__()
        self.init_panel()

    def init_panel(self):
        self.set_scrollable(True)
        self.popup_enable()

        general_grid = Gtk.Grid()
        general_grid.set_border_width(8)
        general_grid.set_column_spacing(10)
        general_grid.attach(Gtk.Label("Enable dark mode"), 0, 0, 1, 1)
        darkmode_btn = Gtk.Switch()
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


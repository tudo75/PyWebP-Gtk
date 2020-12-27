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
import os

from gi import require_version
require_version("Gtk", "3.0")
require_version("Gdk", "3.0")
from gi.repository import Gtk, Gio, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from pywebp.settings import settings
from pywebp.settings_panel import SettingsPanel
from webptools import cwebp, dwebp

LOGO_PATH = os.path.join(os.path.dirname(__file__), 'images/webp-logo.svg')

class PyWebP(Gtk.Application):
    """
    Main Class
    """
    def _init__(self):
        app_id = "com.github.tudo75.pywebp-gtk"
        super(PyWebP, self).__init__(application_id=app_id)
        self.set_flags(Gio.ApplicationFlags.NON_UNIQUE)
        self.connect("activate", self.do_activate)
        self.connect("destroy", self.do_shutdown)
        self.window = None
        self.header_bar = None
        self.iconview = None
        self.toolbar = None
        self.statusbar = None
        self.popover = None

    def do_activate(self):
        """Activate method required
        """
        self._init_widgets()
        self._create_window_structure()
        self._init_style(settings.get_boolean("darkmode"))
        self.add_window(self.window)
        self.window.show_all()

    def do_shutdown(self):
        """Callback when app is closed
        """
        Gtk.Application.do_shutdown(self)
        sys.exit()

    def _create_window_structure(self):
        """Generate the Gui structure
        """
        self.header_bar.set_title("PyWebP-Gtk")
        self.header_bar.set_has_subtitle(False)
        self.header_bar.set_show_close_button(True)
        # self.header_bar.add(Gtk.Image.new_from_file(os.path.join(os.path.dirname(__file__), 'images/icons/logo/32.png')))

        #about_btn = Gtk.Button.new_from_icon_name("application-system", Gtk.IconSize.LARGE_TOOLBAR)
        about_btn = Gtk.Button()
        about_btn.set_image(Gtk.Image.new_from_pixbuf(Pixbuf.new_from_file_at_scale(LOGO_PATH, 32, 32, True)))
        # about_btn.set_image(Gtk.Image.new_from_file(about_icon_path))
        about_btn.connect("clicked", self.on_about)
        self.header_bar.pack_start(about_btn)

        settings_btn = Gtk.Button()
        settings_btn.set_image(Gtk.Image.new_from_icon_name('emblem-system-symbolic', Gtk.IconSize.DND))
        # settings_btn.connect("clicked", self.on_about)
        self.header_bar.pack_end(settings_btn)

        self.init_popover(settings_btn, SettingsPanel())

        self.window.set_titlebar(self.header_bar)

        v_box = Gtk.VBox()
        v_box.add(self.iconview)
        v_box.add(self.toolbar)
        v_box.add(self.statusbar)
        self.window.add(v_box)
        # geometry = settings['geometry'].get_value()
        geometry = settings.get_integer_list("geometry")
        self.window.resize(geometry[0], geometry[1])
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_icon(Pixbuf.new_from_file_at_scale(LOGO_PATH, 32, 32, True))
        self.window.set_default_icon(Pixbuf.new_from_file_at_scale(LOGO_PATH, 32, 32, True))
    
    def _init_widgets(self):
        """Initialize widgets
        """
        self.window = Gtk.Window()
        self.header_bar = Gtk.HeaderBar()
        self.iconview = Gtk.IconView()
        self.toolbar = Gtk.Toolbar()
        self.statusbar = Gtk.Statusbar()

    def _init_style(self, darkmode = True):
        """Load the application's CSS file

        Args:
            darkmode: True or False if you want to use dark mode theme. Default it's True
        """

        print(settings.get_boolean("darkmode"))
        """
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        add_provider = Gtk.StyleContext.add_provider_for_screen
        css_path = os.path.join(os.path.dirname(__file__), 'io.elementary.stylesheet/mint.css')
        if darkmode:
            css_path = os.path.join(os.path.dirname(__file__), 'io.elementary.stylesheet/mint-dark.css')

        provider.load_from_path(css_path)
        add_provider(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        """

    def toggle_darkmode(self, darkmode=True):
        """Want to enable dark mode theme or not

        Args:
            darkmode: True or False if app must use dark mode theme. Default it's True
        """


        # Toggle dark mode for app
        if darkmode:
            self._init_style(True)
        else:
            self._init_style(False)

    def on_about(self, button):
        """Create and display an about us dialog window

        Args:
            button: button who trigger the open action

        Returns:
            a modal about dialog
        """
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True, decorated=True, use_header_bar=True)
        about_dialog.connect("response", self.on_close)

        about_dialog.set_logo(Pixbuf.new_from_file_at_scale(LOGO_PATH, 128, 128, True))
        about_dialog.set_authors(["Nicola Tudino <https://github.com/tudo75>"])
        about_dialog.set_program_name("PyWebP-Gtk")
        about_dialog.set_version('v0.0.1.dev0')
        about_dialog.set_comments('Battery Monitor is a utility tool developed on Python3 and PyGtk3.'
                                  ' It will notify the user about charging, discharging, not charging and critically'
                                  ' low battery state of the battery on Linux (surely if the battery is present).')
        about_dialog.set_website("http://tudo75.github.com/tudo75/PyWebP-Gtk")
        about_dialog.set_website_label("Github Code Repository")
        about_dialog.set_copyright('Copyright \xa9 2020-2021 Tudo75')

        about_dialog.set_documenters(['Maksudur Rahman Maateen <https://maateen.me/>',])
        about_dialog.add_credit_section('Webptools package', ['Sai Kumar Yava <https://github.com/scionoftech>'])
        about_dialog.add_credit_section('Webptools package', ['Sai Kumar Yava <https://github.com/scionoftech>'])

        about_dialog.set_license_type (Gtk.License.MIT_X11)
        about_dialog.set_license('''
MIT License

Copyright (c) 2020-2021 Nicola Tudino <a.k.a. tudo75>

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
''')
        # hack to remove doubled buttons
        hbar = about_dialog.get_header_bar()
        for child in hbar.get_children():
            if type(child) in [Gtk.Button, Gtk.ToggleButton]:
                child.destroy()

        # show the about dialog
        about_dialog.run()
        about_dialog.destroy()

    @staticmethod
    def on_close(action, parameter):
        """ Action to be taken on about dialog close event

        Args:
            action: close action of the about dialog
        """
        action.destroy()

    def init_popover(self, widget, container):
        """Add popover for button.

        Args:
            widget: Popover point to this widget (usually a button)
            container: Container inside the popover
        """
        self.popover = Gtk.Popover()
        self.popover.set_relative_to(widget)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        self.popover.set_modal(True)
        self.popover.add(container)
        self.popover.set_border_width(8)
        self.popover.set_hexpand(False)
        widget.connect("clicked", self.on_click_popup)

    def on_click_popup(self, button):
        """Triggered action to show the popover

        Args:
            button: button that trigger the popup action
        """
        self.popover.popup()

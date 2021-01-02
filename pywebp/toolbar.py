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

from gi import require_version
require_version("Gtk", "3.0")
require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from gi.repository.GdkPixbuf import Pixbuf
from pywebp.helpers import error_message
from pywebp.settings import settings


class Toolbar(Gtk.Toolbar):
    """Toolbar class for PyWebP.

    Inherits from Gtk.Toolbar and includes all actions that apply to it.

    Attributes:
        _app: The main pywebp class to interact with.
    """

    def __init__(self, app):
        super(Toolbar, self).__init__()
        self._app = app
        self.set_icon_size(Gtk.IconSize.BUTTON)
        self.set_style(Gtk.ToolbarStyle.BOTH_HORIZ)
        self.set_show_arrow(False)
        self._init_toolbar()

    def _init_toolbar(self):
        """Initialize toolbar gui

        """
        add_files_btn = Gtk.ToolButton()
        add_files_btn.set_is_important(True)
        add_files_btn.set_label("Add files")
        add_files_btn.set_icon_name("list-add-symbolic")
        add_files_btn.connect('clicked', self.choose_files)
        self.add(add_files_btn)

        separator = Gtk.SeparatorToolItem()
        self.add(separator)
        separator.set_draw(False)
        separator.set_expand(True)

        # TODO implement remove files from thumbs board
        remove_files_btn = Gtk.ToolButton()
        remove_files_btn.set_is_important(True)
        remove_files_btn.set_label_widget(Gtk.Label("Remove files"))
        remove_files_btn.set_icon_name("user-trash-symbolic")
        self.add(remove_files_btn)

        separator = Gtk.SeparatorToolItem()
        self.add(separator)
        separator.set_draw(False)
        separator.set_expand(True)

        # TODO implement handling of select/deselect all thumbs of the board
        select_chk_btn = Gtk.ToolItem()
        select_chk_btn.set_is_important(True)
        chk_all = Gtk.CheckButton.new_with_label('Select All')
        select_chk_btn.add(chk_all)
        self.add(select_chk_btn)

        separator = Gtk.SeparatorToolItem()
        self.add(separator)
        separator.set_draw(False)
        separator.set_expand(True)

        to_from_chk_btn = Gtk.ToolItem()
        to_from_chk_btn.set_is_important(True)
        chk_to_from = Gtk.CheckButton.new_with_label('To WebP')
        chk_to_from.set_active(settings.get_boolean("to_webp"))
        chk_to_from.connect('toggled', self.set_to_webp)
        to_from_chk_btn.add(chk_to_from)
        self.add(to_from_chk_btn)

        separator = Gtk.SeparatorToolItem()
        self.add(separator)
        separator.set_draw(False)
        separator.set_expand(True)

        # TODO implement conversion routines
        convert_btn = Gtk.ToolButton()
        convert_btn.set_is_important(True)
        convert_btn.set_label_widget(Gtk.Label("Convert"))
        convert_btn.set_icon_name("emblem-photos-symbolic")
        self.add(convert_btn)

        self.show_all()

    def choose_files(self, action):
        """Open FileChooserDialog to pick images to be converted

        Args:
            action: component that trigger this callback

        """
        dialog = Gtk.FileChooserDialog(("Choose directory"),
                                       None,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
                                        )
                                       )
        dialog.set_select_multiple(True)

        filter = Gtk.FileFilter()

        to_webp = settings.get_boolean("to_webp")
        if to_webp:
            filter.set_name("Images")
            filter.add_mime_type("image/png")
            filter.add_mime_type("image/jpeg")
            filter.add_mime_type("image/gif")
            filter.add_pattern("*.png")
            filter.add_pattern("*.jpg")
            filter.add_pattern("*.gif")
            filter.add_pattern("*.tif")
            filter.add_pattern("*.xpm")
            dialog.add_filter(filter)
        else:
            filter.set_name("WebP")
            filter.add_mime_type("image/webp")
            filter.add_pattern("*.webp")
            dialog.add_filter(filter)

        dialog.set_default_size(600, 400)
        dialog.set_default_geometry(600, 400)
        dialog.resize(600, 400)

        dialog.connect("update-preview", self.update_preview, None)

        # TODO handling the response to populate thumbs board (check for duplicates)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print(dialog.get_filenames())
        elif response == Gtk.ResponseType.CANCEL:
            print('cancel')

        dialog.destroy()

    def update_preview(self, dialog, image):
        """Handle preview image widget inside FileChooserDialog

        Args:
            dialog: parent FileChooserDialog of the preview component
            image: not used
        """
        dialog.set_preview_widget_active(False)
        filename = dialog.get_preview_filename()
        try:
            if filename is not None:
                if os.path.isfile(filename):
                    # TODO fix error if file is not handled by pixbuf or filter by extension/data correctness
                    _pixbuf = Pixbuf.new_from_file_at_scale(filename, 256, -1, True)
                    have_preview = (_pixbuf != None)
                    img = Gtk.Image.new_from_pixbuf(_pixbuf)
                    dialog.set_preview_widget(img)
                    dialog.set_preview_widget_active(have_preview)
        except GLib.GError as error:
            context_id = self._app.statusbar.get_context_id("error-from-filechooser")
            self._app.push_status_message(error, context_id, 4)

    def set_to_webp(self, action):
        """Register preferences if file conversions to or from webp format

        Args:
            action: toggled widget used to make the choice
        """
        checked = action.get_active()
        if checked:
            settings.set_boolean("to_webp", True)
        else:
            settings.set_boolean("to_webp", False)


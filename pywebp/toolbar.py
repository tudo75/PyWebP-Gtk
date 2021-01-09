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
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from gi.repository.GdkPixbuf import Pixbuf
from pywebp.settings import settings
from pywebp import helpers


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

        remove_files_btn = Gtk.ToolButton()
        remove_files_btn.set_is_important(True)
        remove_files_btn.set_label_widget(Gtk.Label("Remove files"))
        remove_files_btn.set_icon_name("user-trash-symbolic")
        remove_files_btn.connect('clicked', self.remove_files)
        self.add(remove_files_btn)

        separator = Gtk.SeparatorToolItem()
        self.add(separator)
        separator.set_draw(False)
        separator.set_expand(True)

        select_chk_btn = Gtk.ToolItem()
        select_chk_btn.set_is_important(True)
        self._chk_all = Gtk.CheckButton.new_with_label('Select All')
        self._chk_all.connect('toggled', self.select_all)
        select_chk_btn.add(self._chk_all)
        self.add(select_chk_btn)

        separator = Gtk.SeparatorToolItem()
        self.add(separator)
        separator.set_draw(False)
        separator.set_expand(True)

        to_from_chk_btn = Gtk.ToolItem()
        to_from_chk_btn.set_is_important(True)
        self._chk_to_from = Gtk.CheckButton.new_with_label('To WebP')
        self._chk_to_from.set_active(settings.get_boolean("to_webp"))
        self._chk_to_from.connect('toggled', self.set_to_webp)
        to_from_chk_btn.add(self._chk_to_from)
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
        hb = dialog.get_header_bar()
        if not hb == None:        
            hb.set_show_close_button(True)

        dialog.connect("update-preview", self.update_preview, None)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            for img in dialog.get_filenames():
                self._app.iconview._model.add_to_model(img)

            context_id = self._app.statusbar.get_context_id("choose_files")
            self._app.push_status_message("Selected files added", context_id, 4)
            self._chk_to_from.set_sensitive(False)
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

    def set_to_webp(self, checkbox):
        """Register preferences if file conversions to or from webp format

        Args:
            checkbox: toggled widget used to make the choice
        """
        checked = checkbox.get_active()
        msg = "Unable to change file conversion type while files are already added"
        if len(self._app.iconview._model.get_model()) == 0:
            if checked:
                settings.set_boolean("to_webp", True)
                msg = "File conversion set 'to webp'"
            else:
                settings.set_boolean("to_webp", False)
                msg = "File conversion set 'from webp'"

        context_id = self._app.statusbar.get_context_id("set_to_webp")
        self._app.push_status_message(msg, context_id, 4)

    def remove_files(self, btn):
        """

        Args:
            btn:

        Returns:

        """
        msg = "Selected items removed"
        items = self._app.iconview.get_selected_items()
        removed = self._app.iconview._model.remove_selected(items)
        if not removed:
            msg = "Unable to remove some items"

        if len(self._app.iconview._model.get_model()) == 0:
            self._chk_to_from.set_sensitive(True)
            self._app.toolbar.set_select_all(False)

        context_id = self._app.statusbar.get_context_id("remove_files")
        self._app.push_status_message(msg, context_id, 4)


    def select_all(self, checkbox):
        """

        Args:
            checkbox:
        """
        checked = checkbox.get_active()
        msg = ""
        if checked:
            self._app.iconview.select_all()
            msg = "All items selected"
        else:
            self._app.iconview.unselect_all()
            msg = "All items deselected"


        context_id = self._app.statusbar.get_context_id("select_all")
        self._app.push_status_message(msg, context_id, 4)

    def set_select_all(self, value):
        """

        Args:
            value:
        """
        if isinstance(value, (bool)):
            self._chk_all.set_active(value)

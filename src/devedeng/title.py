# Copyright 2014 (C) Raster Software Vigo (Sergio Costas)
#
# This file is part of DeVeDe-NG
#
# DeVeDe-NG is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# DeVeDe-NG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from gi.repository import Gtk, GObject
import os


class title(GObject.GObject):

    counter = 0

    def __init__(self, config, file_treeview, original_liststore, title_name=None):

        GObject.GObject.__init__(self)
        self.config = config
        self.file_treeview = file_treeview
        if (title_name is None):
            title.counter += 1
            self.title_name = _("Title %(X)d") % {"X": title.counter}
        else:
            self.title_name = title_name
        self.post_action = "stop"
        columns = []
        for iterator in range(0, original_liststore.get_n_columns()):
            columns.append(original_liststore.get_column_type(iterator))
        self.files = Gtk.ListStore()
        self.files.set_column_types(columns)

    def set_type(self, disc_type):

        self.disc_type = disc_type

    def properties(self):

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(
            self.config.glade, "wtitle_properties.ui"))
        builder.connect_signals(self)

        # Interface widgets
        wtitle_properties = builder.get_object("title_properties")
        wtitle = builder.get_object("entry_title")
        wplay_first = builder.get_object("play_first")
        wplay_prev = builder.get_object("play_previous")
        wplay_again = builder.get_object("play_again")
        wplay_next = builder.get_object("play_next")
        wplay_last = builder.get_object("play_last")

        wtitle.set_text(self.title_name)
        builder.get_object(self.post_action).set_active(True)

        wtitle_properties.show_all()
        retval = wtitle_properties.run()
        if (retval == 2):
            self.title_name = wtitle.get_text()
            if (wplay_first.get_active()):
                self.post_action = "play_first"
            elif (wplay_prev.get_active()):
                self.post_action = "play_previous"
            elif (wplay_again.get_active()):
                self.post_action = "play_again"
            elif (wplay_next.get_active()):
                self.post_action = "play_next"
            elif (wplay_last.get_active()):
                self.post_action = "play_last"
            else:
                self.post_action = "stop"

        wtitle_properties.destroy()

    def delete_title(self):

        print("Deleted title " + self.title_name)

    def refresh(self):

        self.file_treeview.set_model(self.files)

    def add_file(self, new_file):

        self.files.append([new_file.file_name, new_file])

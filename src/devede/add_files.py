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

from gi.repository import Gtk
import os

class add_files:

    last_path = None

    def __init__(self,config):

        self.config = config
        self.show_title_options = True

    def set_type(self,disc_type):

        if (disc_type == "dvd"):
            self.show_title_options = True
        else:
            self.show_title_options = False

    def run(self):

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(self.config.glade,"wadd_files.ui"))
        builder.connect_signals(self)
        wadd_files = builder.get_object("add_files")
        self.wfile_chooser = builder.get_object("filechooserwidget1")
        if (add_files.last_path != None):
            self.wfile_chooser.set_current_folder(add_files.last_path)
        self.wadd_to_current_title = builder.get_object("add_to_current_title")
        self.wadd_to_new_titles = builder.get_object("add_to_new_titles")
        self.wuse_filename_as_title = builder.get_object("use_filename_as_title")
        self.wbutton_accept = builder.get_object("button_accept")

        woptions = builder.get_object("frame_options")

        wadd_files.show_all()
        if (self.show_title_options == False):
            woptions.hide()

        self.on_add_to_new_titles_toggled(None)
        retval = wadd_files.run()
        self.files = None
        self.add_to_current_title = True
        self.use_filename_as_title = False

        if (retval == 2):
            self.add_to_current_title = self.wadd_to_current_title.get_active()
            self.use_filename_as_title = self.wuse_filename_as_title.get_active()
            self.files = self.get_files()

            print(self.files)

        add_files.last_path = self.wfile_chooser.get_current_folder()
        wadd_files.destroy()

        if (retval == 2):
            return True
        else:
            return False

    def get_files(self):
        files = self.wfile_chooser.get_filenames()
        files_out = []
        for element in files:
            if (os.path.isdir(element)):
                continue
            files_out.append(element)
        return files_out

    def on_filechooserwidget1_selection_changed(self,b):

        files = self.get_files()
        if (len(files) == 0):
            self.wbutton_accept.set_sensitive(False)
        else:
            self.wbutton_accept.set_sensitive(True)

    def on_add_to_new_titles_toggled(self,b):

        self.wuse_filename_as_title.set_sensitive(self.wadd_to_new_titles.get_active())
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
import devedeng.configuration_data


class add_files:

    last_path = None

    def __init__(self):

        self.config = devedeng.configuration_data.configuration.get_config()

    def run(self):

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(self.config.glade, "wadd_files.ui"))
        builder.connect_signals(self)
        wadd_files = builder.get_object("add_files")
        self.wfile_chooser = builder.get_object("filechooserwidget1")
        if (add_files.last_path is not None):
            self.wfile_chooser.set_current_folder(add_files.last_path)
        self.wbutton_accept = builder.get_object("button_accept")

        file_filter_videos = Gtk.FileFilter()
        file_filter_videos.set_name(_("Video files"))
        file_filter_videos.add_mime_type("video/*")
        file_filter_videos.add_pattern("*.rmvb")

        file_filter_all = Gtk.FileFilter()
        file_filter_all.set_name(_("All files"))
        file_filter_all.add_pattern("*")

        self.wfile_chooser.add_filter(file_filter_videos)
        self.wfile_chooser.add_filter(file_filter_all)

        wadd_files.show_all()

        retval = wadd_files.run()
        self.files = None

        if (retval == 2):
            self.files = self.get_files()

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

    def on_filechooserwidget1_selection_changed(self, b):

        files = self.get_files()
        if (len(files) == 0):
            self.wbutton_accept.set_sensitive(False)
        else:
            self.wbutton_accept.set_sensitive(True)

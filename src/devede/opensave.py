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
import devede.configuration_data

class opensave_window:

    def __init__(self, save):

        self.config = devede.configuration_data.configuration.get_config()
        self.save = save


    def run(self,current_file = None):

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        if self.save:
            builder.add_from_file(os.path.join(self.config.glade,"wsave_project.ui"))
        else:
            builder.add_from_file(os.path.join(self.config.glade,"wopen_project.ui"))
        builder.connect_signals(self)
        w_window = builder.get_object("data_project")
        if current_file != None:
            w_window.set_filename(current_file)

        file_filter_projects=Gtk.FileFilter()
        file_filter_projects.set_name(_("DevedeNG projects"))
        file_filter_projects.add_pattern("*.devedeng")

        file_filter_all=Gtk.FileFilter()
        file_filter_all.set_name(_("All files"))
        file_filter_all.add_pattern("*")

        w_window.add_filter(file_filter_projects)
        w_window.add_filter(file_filter_all)

        w_window.show_all()
        retval = w_window.run()
        self.final_filename = w_window.get_filename()
        w_window.destroy()
        if (retval == 1):
            return self.final_filename
        else:
            return None
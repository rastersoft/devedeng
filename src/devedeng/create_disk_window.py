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

class create_disk_window:

    def __init__(self):

        self.config = devedeng.configuration_data.configuration.get_config()

    def run(self):

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(self.config.glade,"wcreate.ui"))
        builder.connect_signals(self)
        wcreate_window = builder.get_object("dialog_create")
        self.wpath = builder.get_object("path")
        self.wname = builder.get_object("name")
        wshutdown = builder.get_object("shutdown")
        self.waccept = builder.get_object("accept")

        self.wname.set_text("movie")
        self.wpath.set_current_folder(self.config.final_folder)

        wcreate_window.show_all()
        self.on_iface_changed(None)
        retval = wcreate_window.run()
        self.name = self.wname.get_text()
        self.path = os.path.join(self.wpath.get_filename(),self.name)
        self.shutdown = wshutdown.get_active()

        if (retval == 1):
            self.config.final_folder = self.wpath.get_filename()
            self.config.save_config()

        wcreate_window.destroy()
        if (retval == 1):
            return True
        else:
            return False
    
    def on_iface_changed(self,b):
        
        path = self.wpath.get_filename()
        name = self.wname.get_text()
        
        if ((path is None) or (path == "") or (name is None) or (name == "")):
            self.waccept.set_sensitive(False)
        else:
            self.waccept.set_sensitive(True)

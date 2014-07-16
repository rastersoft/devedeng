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

from gi.repository import Gtk,GObject
import os

import devede.configuration_data

class choose_disc_type(GObject.GObject):
    
    def __init__(self):

        self.config  = devede.configuration_data.configuration.get_config()

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(self.config.glade,"wselect_disk.ui"))
        builder.connect_signals(self)
        self.wask_window = builder.get_object("wselect_disk")
        self.wask_window.show_all()

    def set_type(self,disc_type):
        
        self.config.set_disc_type(disc_type)
        self.wask_window.hide()
        self.wask_window.destroy()
        self.wask_window = None

    def on_button_dvd_clicked(self,b):

        self.set_type("dvd")

    def on_button_vcd_clicked(self,b):

        self.set_type("vcd")

    def on_button_svcd_clicked(self,b):

        self.set_type("svcd")

    def on_button_cvd_clicked(self,b):

        self.set_type("cvd")

    def on_button_divx_clicked(self,b):

        self.set_type("divx")

    def on_button_mkv_clicked(self,b):

        self.set_type("mkv")

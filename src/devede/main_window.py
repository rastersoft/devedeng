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

class choose_disk:
    
    def __init__(self,paths):

        self.paths = paths
        
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain("devede_ng")
        
        self.builder.add_from_file(os.path.join(paths.glade,"wselect_disk.ui"))
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("wselect_disk")
        
        self.window.show_all()

    def main_window(self,disk_type):
        
        self.window.hide()
        self.window.destroy()
        self.main_window = main_window(self.paths,disk_type)
        

    def on_button_dvd_clicked(self,b):
        
        self.main_window("dvd")
    
    def on_button_vcd_clicked(self,b):
        
        self.main_window("vcd")
    
    def on_button_svcd_clicked(self,b):
        
        self.main_window("svcd")
    
    def on_button_cvd_clicked(self,b):
        
        self.main_window("cvd")
    
    def on_button_divx_clicked(self,b):
        
        self.main_window("divx")

    def on_wselect_disk_delete_event(self,w,e):
        Gtk.main_quit()
        return False



class main_window:
    
    def __init__(self,paths,disk_type):
        
        self.paths = paths
        self.disk_type = disk_type
        
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain("devede_ng")
        
        self.builder.add_from_file(os.path.join(paths.glade,"wmain.ui"))
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("wmain")
        
        self.window.show_all()
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

class file_movie(GObject.GObject):

    counter2 = 0

    def __init__(self,config,file_name):

        GObject.GObject.__init__(self)
        self.config = config
        self.file_name = file_name
        self.title_name =  os.path.splitext(os.path.basename(file_name))[0]
        self.wfile_properties = None
        self.model = None
        self.treeiter = None
        self.builder = None

    def set_type(self,disc_type = None):

        if (disc_type != None):
            self.disc_type = disc_type
        

    def delete_file(self):

        print("Deleted file "+self.file_name)

    def properties(self,model,treeiter):
        
        if (self.wfile_properties != None):
            self.wfile_properties.present()
            return
        
        self.model = model
        self.treeiter = treeiter
        
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(self.config.gettext_domain)

        self.builder.add_from_file(os.path.join(self.config.glade,"wfile_properties.ui"))
        self.builder.connect_signals(self)
        self.wfile_properties = self.builder.get_object("file_properties")
        self.wfile_properties.show_all()
    
        self.wfile = self.builder.get_object("label_filename")
        self.wtitle = self.builder.get_object("entry_title")
        
        self.wfile.set_text(self.file_name)
        self.wtitle.set_text(self.title_name)
    
    def on_button_accept_clicked(self,b):
        
        
        self.title_name = self.wtitle.get_text()
        self.model.set_value(self.treeiter,1,self.title_name)
        self.on_button_cancel_clicked(None)
    
    def on_button_cancel_clicked(self,b):
        
        self.wfile_properties.destroy()
        self.wfile_properties = None
        self.builder = None
        self.model = None
        self.treeiter = None

        
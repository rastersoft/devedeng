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
import devede.interface_manager

class dvd_menu(devede.interface_manager.interface_manager):

    def __init__(self):

        devede.interface_manager.interface_manager.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()

        self.add_toggle("dynamic_preview", self.config.menu_dynamic_preview)

        self.add_colorbutton("title_color", (0,0,0,1), self.update_preview)
        self.add_colorbutton("title_shadow", (0,0,0,0), self.update_preview)
        self.add_colorbutton("unselected_color", (1,1,1,1), self.update_preview)
        self.add_colorbutton("shadow_color", (0,0,0,0), self.update_preview)
        self.add_colorbutton("selected_color", (0,1,1,1), self.update_preview)
        self.add_colorbutton("background_color", (0,0,0,0.75), self.update_preview)
        
        self.add_text("title_text", None, self.update_preview)
        
        self.add_group("position_vertical", ["top", "middle", "bottom"], "middle", self.update_preview)
        self.add_group("position_horizontal", ["left", "center", "right"], "center", self.update_preview)
        
        self.add_float_adjustment("margin_left", 10.0, self.update_preview)
        self.add_float_adjustment("margin_top", 12.5, self.update_preview)
        self.add_float_adjustment("margin_right", 10.0, self.update_preview)
        self.add_float_adjustment("margin_bottom", 12.5, self.update_preview)
        
        self.add_group("at_startup", ["menu_show_at_startup", "play_first_title_at_startup"], "menu_show_at_startup")
        
    def update_preview(self,b=None):
        
        print("Cambiado algo")

    def on_dynamic_preview_toggled(self,b):
        
        self.config.menu_dynamic_preview = self.wdynamic_preview.get_active()
        if (self.config.menu_dynamic_preview):
            self.wframe_preview.show_all()
        else:
            self.wframe_preview.hide()


    def show_configuration(self):

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(self.config.gettext_domain)

        self.builder.add_from_file(os.path.join(self.config.glade,"wmenu.ui"))
        self.builder.connect_signals(self)

        self.wdynamic_preview = self.builder.get_object("dynamic_preview")
        self.wframe_preview = self.builder.get_object("frame_preview")
        self.wmenu = self.builder.get_object("menu")

        self.wmenu.show_all()

        self.update_ui(self.builder)
        self.on_dynamic_preview_toggled(None)


    def on_accept_clicked(self,b):

        self.store_ui(self.builder)
        self.wmenu.destroy()
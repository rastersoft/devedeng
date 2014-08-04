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
import gettext
import devede.converter

class settings_window(devede.interface_manager.interface_manager):

    def __init__(self):

        devede.interface_manager.interface_manager.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()

        if (self.config.multicore > 0):
            if self.config.cores < self.config.multicore:
                cores = self.config.cores
            else:
                cores = self.config.multicore
        else:
            if self.config.cores <= -self.config.multicore:
                cores = -self.config.cores+1
            else:
                cores = self.config.multicore

        self.core_elements = {}
        list_core_elements = []
        default_value = _("Use all cores")
        counter = 1
        for c in range(self.config.cores-1,-self.config.cores, -1):
            if c > 0:
                translated_string = gettext.ngettext("Use %(X)d core","Use %(X)d cores",c) % {"X":c}
                value = c
                if c == cores:
                    default_value = translated_string
                counter += 1
            elif c < 0:
                translated_string = gettext.ngettext("Use all except %(X)d core","Use all except %(X)d cores", -c) % {"X": -c}
                value = c
                if c == cores:
                    default_value = translated_string
                counter += 1
            else:
                translated_string = _("Use all cores")
                value = c

            self.core_elements[translated_string] = value
            list_core_elements.append(translated_string)

        self.add_combobox("multicore",list_core_elements,default_value)
        self.add_filebutton("tempo_path", self.config.tmp_folder)

        c = devede.converter.converter.get_converter()
        (analizers, players, menuers, converters, burners) = c.get_available_programs()

        self.add_combobox("analizer", analizers,self.config.film_analizer)
        self.add_combobox("player", players,self.config.film_player)
        self.add_combobox("converter", converters,self.config.film_converter,self.set_data_converter)
        self.add_combobox("menuer", menuers,self.config.menu_converter)
        self.add_combobox("burner", burners, self.config.burner)

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(self.config.gettext_domain)

        self.builder.add_from_file(os.path.join(self.config.glade,"wsettings.ui"))
        self.builder.connect_signals(self)
        wsettings_window = self.builder.get_object("settings")
        self.wconverter = self.builder.get_object("converter")
        self.wtypes = self.builder.get_object("disc_types_supported")

        wsettings_window.show_all()
        self.update_ui(self.builder)
        self.set_data_converter(None)

        retval = wsettings_window.run()
        self.store_ui(self.builder)
        wsettings_window.destroy()

        if retval == 1:
            self.config.multicore = self.core_elements[self.multicore]
            self.config.tmp_folder = self.tempo_path
            self.config.film_analizer = self.analizer
            self.config.film_player = self.player
            self.config.film_converter = self.converter
            self.config.menu_converter = self.menuer
            self.config.burner = self.burner
            self.config.save_config()

    def set_data_converter(self,b):

        self.store_ui(self.builder)
        cv = devede.converter.converter.get_converter()
        cv2 = cv.get_disc_converter_by_name(self.converter)
        data = ""
        for t in cv2.disc_types:
            if data != "":
                data += ", "
            data += t
        if data != "":
            self.wtypes.set_text(data)
        else:
            self.wtypes.set_text(_("No discs supported"))
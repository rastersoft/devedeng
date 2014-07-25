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

import devede.configuration_data
import devede.mplayer_detector
import devede.avconv_converter

class converter:

    current_converter = None

    @staticmethod
    def get_converter():
        if converter.current_converter == None:
            converter.current_converter = converter.converter()
        return converter.current_converter


    def __init__(self):

        self.config = devede.configuration_data.configuration.get_config()
        # List of classes with conversion capabilities, in order of preference
        self.c = [devede.mplayer_detector.mplayer_detector, devede.avconv_converter.avconv_converter]

        self.analizers = {}
        self.default_analizer = None
        self.players = {}
        self.default_player = None
        self.converters = {}
        self.default_converter = None
        self.menuers = {}
        self.default_menuer = None
        self.discs = []

        for element in self.c:
            if (element.check_is_installed() == False):
                continue
            name = element.display_name
            if (element.supports_analize):
                self.analizers[name] = element
                if (self.default_analizer == None):
                    self.default_analizer = element
            if (element.supports_play):
                self.players[name] = element
                if (self.default_player == None):
                    self.default_player = element
            if (element.supports_convert):
                self.converters[name] = element
                if (self.default_converter == None):
                    self.default_converter = element
                for types in element.disc_types:
                    if self.discs.count(types) == 0:
                        self.discs.append(types)
            if (element.supports_menu):
                self.menuers[name] = element
                if (self.default_menuer == None):
                    self.default_menuer = element


    def get_needed_programs(self):
        """ returns a tupla with four lists. When a list is NONE, there are installed in the system
            programs that covers the needs for that group; when not, it contains the programs valid
            to cover the needs for that group.
            The groups are, in this order: ANALIZERS, PLAYERS, CONVERTERS, MENUERS
            (menuers are the programs that creates the mpeg files for menus) """

        if (self.default_analizer != None):
            analizers = None
        else:
            analizers = []
        if (self.default_player != None):
            players = None
        else:
            players = []
        if (self.default_converter != None):
            converters = None
        else:
            converters = []
        if (self.default_menuer != None):
            menuers = None
        else:
            menuers = []

        for element in self.c:
            e = element()
            name = e.display_name
            if (e.supports_analize) and (analizers != None):
                analizers.append(name)
            if (e.supports_play) and (players != None):
                players.append(name)
            if (e.supports_convert) and (converters != None):
                converters.append(name)
            if (e.supports_menu) and (menuers != None):
                menuers.append(name)

        return ( analizers, players, converters, menuers )


    def get_film_analizer(self):
        """ returns a class for the desired film analizer, or the most priviledged if the desired is not installed """

        if (self.config.film_analizer == None) or (self.analizers.has_key(self.config.film_analizer) == False):
            return self.default_analizer
        else:
            return self.analizers[self.config.film_analizer]

    def get_menu_converter(self):
        """ returns a class for the desired menu converter, or the most priviledged if the desired is not installed """

        if (self.config.menu_converter == None) or (self.analizers.has_key(self.config.menu_converter) == False):
            return self.default_menuer
        else:
            return self.menuers[self.config.menu_converter]
    
    def get_disc_converter(self):
        """ returns a class for the desired disc converter, or the most priviledged if the desired is not installed """

        if (self.config.film_converter == None) or (self.analizers.has_key(self.config.film_converter) == False):
            return self.default_converter
        else:
            return self.converters[self.config.film_converter]
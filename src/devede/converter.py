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
import devede.vlc
import devede.brasero
import devede.k3b

class converter:

    current_converter = None

    @staticmethod
    def get_converter():
        if converter.current_converter == None:
            converter.current_converter = converter()
        return converter.current_converter


    def __init__(self):

        self.config = devede.configuration_data.configuration.get_config()
        # List of classes with conversion capabilities, in order of preference
        self.c = [devede.vlc.vlc_player, devede.mplayer_detector.mplayer_detector, devede.avconv_converter.avconv_converter,
                  devede.brasero.brasero, devede.k3b.k3b]

        self.analizers = {}
        self.default_analizer = None
        self.players = {}
        self.default_player = None
        self.converters = {}
        self.default_converter = None
        self.menuers = {}
        self.default_menuer = None
        self.burners = {}
        self.default_burner = None
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
            if (element.supports_burn):
                self.burners[name] = element
                if (self.default_burner == None):
                    self.default_burner = element

    def get_available_programs(self):

        players = []
        menuers = []
        converters = []
        analizers = []
        burners = []

        for e in self.analizers:
            analizers.append(e)
        for e in self.players:
            players.append(e)
        for e in self.menuers:
            menuers.append(e)
        for e in self.converters:
            converters.append(e)
        for e in self.burners:
            burners.append(e)

        return (analizers, players, menuers, converters, burners)

    def get_needed_programs(self):
        """ returns a tupla with four lists. When a list is NONE, there are installed in the system
            programs that covers the needs for that group; when not, it contains the programs valid
            to cover the needs for that group.
            The groups are, in this order: ANALIZERS, PLAYERS, CONVERTERS, MENUERS, BURNERS
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
        if (self.default_burner != None):
            burners = None
        else:
            burners = []

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
            if (e.supports_burn) and (burners != None):
                burners.append(name)

        return ( analizers, players, converters, menuers, burners )

    def get_film_player(self):
        """ returns a class for the desired film player, or the most priviledged if the desired is not installed """

        if (self.config.film_player == None) or (self.config.film_player not in self.players):
            return self.default_player
        else:
            return self.players[self.config.film_player]

    def get_film_analizer(self):
        """ returns a class for the desired film analizer, or the most priviledged if the desired is not installed """

        if (self.config.film_analizer == None) or (self.config.film_analizer not in self.analizers):
            return self.default_analizer
        else:
            return self.analizers[self.config.film_analizer]

    def get_menu_converter(self):
        """ returns a class for the desired menu converter, or the most priviledged if the desired is not installed """

        if (self.config.menu_converter == None) or (self.config.menu_converter not in self.menuers):
            return self.default_menuer
        else:
            return self.menuers[self.config.menu_converter]

    def get_disc_converter(self):
        """ returns a class for the desired disc converter, or the most priviledged if the desired is not installed """

        # if there is a film converter chosen by the user, and it is installed in the system
        if (self.config.film_converter != None) and (self.config.film_converter in self.converters):
            # and that converter supports the current disc type
            if self.converters[self.config.film_converter].disc_types.count(self.config.disc_type) != 0:
                # return that converter
                return self.converters[self.config.film_converter]
        # if not, return the first available converter that supports the current disc type
        for converter in self.converters:
            if converter.disc_types.count(self.config.disc_type) != 0:
                return converter
        return None
            

    def get_burner(self):
        """ returns a class for the desired burner, or the most priviledged if the desired is not installed """

        if (self.config.burner == None) or (self.config.burner not in self.burners):
            return self.default_burner
        else:
            return self.burners[self.config.burner]
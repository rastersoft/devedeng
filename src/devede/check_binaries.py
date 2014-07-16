#!/usr/bin/env python3

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

import subprocess

import devede.configuration_data

class check_binaries:

    def __init__(self):

        self.config = devede.configuration_data.configuration.get_config()

        self.check_mplayer()
        self.check_mpv()


    def check_mplayer(self):

        handle = subprocess.Popen(["mplayer","-v"])
        if 0==handle.wait():
            self.config.mplayer_available = True
        else:
            self.config.mplayer_available = False

    def check_mpv(self):

        handle = subprocess.Popen(["mpv","-v"])
        if 0==handle.wait():
            self.config.mpv_available = True
        else:
            self.config.mpv_available = False
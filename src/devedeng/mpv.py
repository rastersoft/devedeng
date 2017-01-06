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
import devedeng.configuration_data
import devedeng.executor


class mpv(devedeng.executor.executor):

    supports_analize = False
    supports_play = True
    supports_convert = False
    supports_menu = False
    supports_mkiso = False
    supports_burn = False
    display_name = "MPV"

    @staticmethod
    def check_is_installed():
        try:
            handle = subprocess.Popen(
                ["mpv", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = handle.communicate()
            if 0 == handle.wait():
                return True
            else:
                return False
        except:
            return False

    def __init__(self):

        devedeng.executor.executor.__init__(self)
        self.config = devedeng.configuration_data.configuration.get_config()

    def play_film(self, file_name):

        command_line = ["mpv", file_name]
        self.launch_process(command_line)

    def process_stdout(self, data):
        return

    def process_stderr(self, data):
        return

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
import devede.executor

class k3b(devede.executor.executor):

    supports_analize = False
    supports_play = False
    supports_convert = False
    supports_menu = False
    supports_mkiso = False
    supports_burn = True
    display_name = "K3B"

    @staticmethod
    def check_is_installed():
        try:
            handle = subprocess.Popen(["k3b","--help"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            (stdout, stderr) = handle.communicate()
            if 0==handle.wait():
                return True
            else:
                return False
        except:
            return False

    def __init__(self):

        devede.executor.executor.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()

    def burn(self,file_name):

        self.command_var = ["k3b", file_name]

    def process_stdout(self,data):
        return

    def process_stderr(self,data):
        return

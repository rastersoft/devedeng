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

import os
import devede.configuration_data
import subprocess
import devede.executor

class mkisofs(devede.executor.executor):

    supports_analize = False
    supports_play = False
    supports_convert = False
    supports_menu = False
    supports_mkiso = True
    supports_burn = False
    display_name = "MKISOFS"

    @staticmethod
    def check_is_installed():
        try:
            handle = subprocess.Popen(["mkisofs","--help"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
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

    def create_iso (self, path, name):

        filesystem_path = os.path.join(path,name)
        final_path = os.path.join(path,name+".iso")

        self.command_var=[]
        self.command_var.append("mkisofs")
        self.command_var.append("-dvd-video")
        self.command_var.append("-V")
        self.command_var.append("DVDVIDEO")
        self.command_var.append("-v")
        self.command_var.append("-udf")
        self.command_var.append("-o")
        self.command_var.append(final_path)
        self.command_var.append(filesystem_path)
        self.text = _("Creating ISO image")


    def process_stdout(self,data):
        return

    def process_stderr(self,data):

        if (data[0].find("% done") == -1):
            return

        l = data[0].split("%")
        p = float(l[0])
        self.progress_bar[1].set_fraction(p/100.0)
        self.progress_bar[1].set_text("%.1f%%" % (p))

        return

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
import os
import devede.configuration_data
import devede.executor

class avconv_converter(devede.executor.executor):

    supports_analize = False
    supports_play = False
    supports_convert = False
    supports_menu = True
    display_name = "AVCONV"

    @staticmethod
    def check_is_installed():
        handle = subprocess.Popen(["avconv","-version"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        (stdout, stderr) = handle.communicate()
        if 0==handle.wait():
            return True
        else:
            return False

    def __init__(self):

        devede.executor.executor.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()

    def create_mpg(self,n_page,background_music,sound_length,pal,output_path):

        self.n_page = n_page
        self.sound_length = float(sound_length)
        self.text = _("Creating menu %(X)d") % {"X": self.n_page}

        self.command_var=[]
        self.command_var.append("avconv")

        self.command_var.append("-loop")
        self.command_var.append("1")

        self.command_var.append("-f")
        self.command_var.append("image2")
        self.command_var.append("-i")
        self.command_var.append(os.path.join(output_path,"menu_"+str(n_page)+"_bg.png"))
        self.command_var.append("-i")
        self.command_var.append(background_music)

        self.command_var.append("-y")
        self.command_var.append("-target")
        if pal:
            self.command_var.append("pal-dvd")
        else:
            self.command_var.append("ntsc-dvd")
        self.command_var.append("-acodec")
        self.command_var.append("mp2")
        self.command_var.append("-s")
        if pal:
            self.command_var.append("720x576")
        else:
            self.command_var.append("720x480")
        self.command_var.append("-g")
        self.command_var.append("12")
        self.command_var.append("-b:v")
        self.command_var.append("2500k")
        self.command_var.append("-b:a")
        self.command_var.append("192k")
        self.command_var.append("-aspect")
        self.command_var.append("4:3")

        self.command_var.append("-t")
        self.command_var.append(str(1+sound_length))

        self.command_var.append(os.path.join(output_path,"menu_"+str(n_page)+".mpg"))

    def process_stdout(self,data):

        pass

    def process_stderr(self,data):

        pos = data[0].find("time=")
        if (pos != -1):
            pos+=5
            pos2 = data[0].find(" ",pos)
            if (pos2 != -1):
                t = float(data[0][pos:pos2])
                self.progress_bar[1].set_fraction(t / self.sound_length)
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
import devedeng.configuration_data
import devedeng.executor


class vcdimager_converter(devedeng.executor.executor):

    def __init__(self):

        devedeng.executor.executor.__init__(self)
        self.config = devedeng.configuration_data.configuration.get_config()

    def create_cd_project(self, path, name, file_movies):

        self.command_var = []
        self.command_var.append("vcdimager")
        self.command_var.append("-c")
        self.command_var.append(os.path.join(path, name + ".cue"))
        self.command_var.append("-b")
        self.command_var.append(os.path.join(path, name + ".bin"))
        self.command_var.append("-t")
        if self.config.disc_type == "vcd":
            self.command_var.append("vcd2")
        else:
            self.command_var.append("svcd")
        for element in file_movies:
            self.command_var.append(element.converted_filename)
        self.text = _("Creating CD image")

    def process_stdout(self, data):
        print("Stdout: " + str(data))
        return

    def process_stderr(self, data):
        print("Stderr: " + str(data))
        return

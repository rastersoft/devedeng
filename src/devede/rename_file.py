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
import devede.executor

class rename_file(devede.executor.executor):

    def __init__(self):

        devede.executor.executor.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()

    def rename(self,file_path_input, file_path_output):

        self.text = _("Renaming %(L)s to %(X)s") % {"X": os.path.basename(file_path_output), "L": os.path.basename(file_path_input)}

        self.command_var=[]
        self.command_var.append("mv")
        self.command_var.append("-f")
        self.command_var.append(file_path_input)
        self.command_var.append(file_path_output)
        self.use_pulse_mode = True

    def process_stdout(self,data):

        return

    def process_stderr(self,data):

        return
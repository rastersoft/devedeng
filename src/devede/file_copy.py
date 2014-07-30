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

class file_copy(devede.executor.executor):

    def __init__(self,input_path, output_path):

        devede.executor.executor.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()

        self.text = _("Copying file %(X)s") % {"X": os.path.basename(input_path)}

        self.command_var=[]
        self.command_var.append("cp")
        self.command_var.append(input_path)
        self.command_var.append(output_path)
        self.use_pulse_mode = True

    def process_stdout(self,data):

        return

    def process_stderr(self,data):

        return
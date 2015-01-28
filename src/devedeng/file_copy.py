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

class file_copy(devedeng.executor.executor):

    def __init__(self,input_path, output_path):

        devedeng.executor.executor.__init__(self)
        self.config = devedeng.configuration_data.configuration.get_config()

        self.text = _("Copying file %(X)s") % {"X": os.path.basename(input_path)}

        self.command_var=[]
        self.command_var.append("copy_files_verbose.py")
        self.command_var.append(input_path)
        self.command_var.append(output_path)


    def process_stdout(self,data):

        if (data == None) or (len(data) == 0):
            return
        if (data[0].startswith("Copied ")):
            pos = data[0].find("%")
            if (pos == -1):
                return
            p = float(data[0][7:pos])
            self.progress_bar[1].set_fraction(p/ 100.0)
            self.progress_bar[1].set_text("%.1f%%" % (p))
        return

    def process_stderr(self,data):

        return
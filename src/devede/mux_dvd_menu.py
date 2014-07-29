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

class mux_dvd_menu(devede.executor.executor):

    def __init__(self):

        devede.executor.executor.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()

    def create_mpg(self,n_page,output_path,movie_path):

        self.n_page = n_page
        self.text = _("Mixing menu %(X)d") % {"X": self.n_page}

        final_path = os.path.join(output_path,"menu_"+str(n_page)+"B.mpg")

        self.command_var=[]
        self.command_var.append("spumux")
        self.command_var.append(os.path.join(output_path,"menu_"+str(n_page)+".xml"))
        self.stdin_file = movie_path
        self.stdout_file = final_path

        return final_path

    def process_stderr(self,data):

        return
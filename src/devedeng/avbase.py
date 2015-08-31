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

import devedeng.executor
import subprocess

class avbase(devedeng.executor.executor):

    def check_version(self,cmd):

        try:
            handle = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            (stdout, stderr) = handle.communicate()
            if 0 != handle.wait():
                return False
        except:
            return False
        self.check_version_txt(stdout)


    def check_version_txt(self,vtext):

        self.major_version = 0
        self.minor_version = 0
       
        for line in vtext:
            if not isinstance(line, str):
                continue
            if (line.startswith("avconv version")):
                pos1 = line.find('.',15)
                pos2 = line.find('-',15)
                if (pos2 == -1):
                    return False
                try:
                    if (pos1 == -1):
                        major = int(line[15:pos2].strip())
                        minor = 0
                    else:
                        major = int(line[15:pos1].strip())
                        minor = int(line[pos1+1:pos2].strip())
                except:
                    return False
                self.major_version = major
                self.minor_version = minor
                return True
        return False

        

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

import sys
import os

if len(sys.argv) != 3:
    print("Usage: copy_files_verbose input_file output_file")
    sys.exit(-1)

filesize = os.path.getsize(sys.argv[1])
done = 0.0
f1 = open(sys.argv[1],"rb")
f2 = open(sys.argv[2],"wb")

while (done < filesize):
    data = f1.read(65536)
    f2.write(data)
    done += len(data)
    print("Copied %.1f%%" % (100.0 * float(done)/float(filesize)))

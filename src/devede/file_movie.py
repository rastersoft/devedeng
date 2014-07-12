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

from gi.repository import GObject

class file_movie(GObject.GObject):

    counter2 = 0

    def __init__(self,paths,file_name):

        GObject.GObject.__init__(self)
        self.paths = paths
        self.file_name = file_name

    def set_type(self,disc_type):

        self.disc_type = disc_type

    def delete_file(self):

        print("Deleted file "+self.file_name)

    def properties(self):

        file_movie.counter2 += 1
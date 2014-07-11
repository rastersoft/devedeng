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

from gi.repository import Gtk,GObject

class title(GObject.GObject):

    counter = 0

    def __init__(self,file_treeview,original_liststore):

        GObject.GObject.__init__(self)
        self.file_treeview = file_treeview
        title.counter += 1
        self.title_name = _("Title %(X)d") % {"X":title.counter}
        columns = []
        for iterator in range(0, original_liststore.get_n_columns()):
            columns.append(original_liststore.get_column_type(iterator))
        self.files = Gtk.ListStore()
        self.files.set_column_types(columns)

    def set_type(self,disc_type):

        self.disc_type = disc_type

    def delete_title(self):

        print("Deleted title "+self.title_name)

    def refresh(self):

        self.file_treeview.set_model(self.files)

    def add_file(self,new_file):

        self.files.append([new_file.file_name, new_file])

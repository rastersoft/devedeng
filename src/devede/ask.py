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

from gi.repository import Gtk
import os

class ask_window:

    def __init__(self,paths):

        self.paths = paths

    def run(self,text,title):

        builder = Gtk.Builder()
        builder.set_translation_domain("devede_ng")

        builder.add_from_file(os.path.join(self.paths.glade,"wask.ui"))
        builder.connect_signals(self)
        wask_window = builder.get_object("dialog_ask")
        wask_window.set_title(title)
        wask_text = builder.get_object("label_ask")
        wask_text.set_markup(text)

        wask_window.show_all()
        retval = wask_window.run()
        wask_window.destroy()
        if (retval == 1):
            return True
        else:
            return False
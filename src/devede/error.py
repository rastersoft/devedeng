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

from gi.repository import Gtk,Gdk
import os
import devede.configuration_data

class error_window:

    def __init__(self):

        self.config = devede.configuration_data.configuration.get_config()

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(self.config.glade,"werror.ui"))
        builder.connect_signals(self)
        werror_window = builder.get_object("dialog_error")
        wdebug_buffer = builder.get_object("debug_buffer")
        wdebug_buffer.insert_at_cursor(self.config.get_log())

        werror_window.show_all()
        werror_window.run()
        werror_window.destroy()


    def on_copy_clicked(self,b):
        
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        data =self.config.get_log()
        clipboard.set_text(data,len(data))
        return

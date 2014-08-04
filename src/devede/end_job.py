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

class end_window:

    def __init__(self):

        self.config = devede.configuration_data.configuration.get_config()

    def run(self,time_used, do_burn):

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(self.config.glade,"wdone.ui"))
        builder.connect_signals(self)
        werror_window = builder.get_object("done")
        wburn = builder.get_object("button_burn")
        wdebug_buffer = builder.get_object("debug_buffer")
        wdebug_buffer.insert_at_cursor(self.config.get_log())
        wtime = builder.get_object("label_time")
        hours = int(time_used / 3600)
        minutes = int((time_used / 60) % 60)
        seconds = int(time_used % 60)
        time_used_str = ""
        if hours < 10:
            time_used_str += "0"
        time_used_str += str(hours)+":"
        if minutes < 10:
            time_used_str += "0"
        time_used_str += str(minutes)+":"
        if seconds < 10:
            time_used_str += "0"
        time_used_str += str(seconds)
        wtime.set_text(time_used_str)

        werror_window.show_all()

        if do_burn:
            wburn.show()
        else:
            wburn.hide()

        retval = werror_window.run()
        werror_window.destroy()
        if retval == 1:
            return True # burn disc image
        else:
            return False


    def on_copy_clicked(self,b):

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        data =self.config.get_log()
        clipboard.set_text(data,len(data))
        return

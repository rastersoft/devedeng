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

class configuration:

    def __init__(self):

        self.error = False
        is_local = None

        try:
            os.stat("/usr/share/devede_ng/wselect_disk.ui")
            is_local = False
        except:
            pass
        
        if is_local == None:
            try:
                os.stat("/usr/local/share/devede_ng/wselect_disk.ui")
                is_local = True
            except:
                pass
        
        if is_local == None:
            self.error = True
        else:
            if (is_local):
                # locales must be always at /usr/share/locale because Gtk.Builder always search there
                self.share_locale="/usr/share/locale"
                self.glade="/usr/local/share/devede_ng"
                self.font_path="/usr/local/share/devede_ng"
                self.pic_path="/usr/local/share/devede_ng"
                self.other_path="/usr/local/share/devede_ng"
                self.help_path="/usr/local/share/doc/devede_ng"
            else:
                self.share_locale="/usr/share/locale"
                self.glade="/usr/share/devede_ng"
                self.font_path="/usr/share/devede_ng"
                self.pic_path="/usr/share/devede_ng"
                self.other_path="/usr/share/devede_ng"
                self.help_path="/usr/share/doc/devede_ng"

        self.gettext_domain = "devede_ng"

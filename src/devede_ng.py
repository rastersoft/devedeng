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
import gettext
import locale
import devede.devede

class config_paths:
    
    def __init__(self,is_local):
        
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
            
            

paths = None

try:
    os.stat("/usr/share/devede_ng/wselect_disk.ui")
    paths = config_paths(False)
except:
    pass

if paths == None:
    try:
        os.stat("/usr/local/share/devede_ng/wselect_disk.ui")
        paths = config_paths(True)
    except:
        pass

if paths == None:
    print ("Can't locate extra files. Aborting.")
    sys.exit(1)

gettext.bindtextdomain('devede_ng',paths.share_locale)
try:
    locale.setlocale(locale.LC_ALL,"")
except locale.Error:
    pass
gettext.textdomain('devede_ng')
gettext.install("devede_ng",localedir=paths.share_locale)  

_ = gettext.gettext

devede.devede.main(sys.argv,paths)
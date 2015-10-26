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

import gi
gi.require_version('Gtk', '3.0')
import sys
import gettext
import locale
from gi.repository import Gtk

import devedeng.project
import devedeng.configuration_data
import devedeng.choose_disc_type

config_data = devedeng.configuration_data.configuration.get_config()

if config_data == None:
    print ("Can't locate extra files. Aborting.")
    sys.exit(1)

gettext.bindtextdomain(config_data.gettext_domain,config_data.share_locale)
try:
    locale.setlocale(locale.LC_ALL,"")
except locale.Error:
    pass
gettext.textdomain(config_data.gettext_domain)
gettext.install(config_data.gettext_domain,localedir=config_data.share_locale)

_ = gettext.gettext

Gtk.init(sys.argv)

mwindow = devedeng.project.devede_project()
ask_type = devedeng.choose_disc_type.choose_disc_type()

Gtk.main()
config_data.save_config()

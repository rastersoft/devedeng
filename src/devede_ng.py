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
import gettext
import locale
from gi.repository import Gtk

import devede.project
import devede.configuration_data

config_data = devede.configuration_data.configuration()

if config_data.error:
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

mwindow = devede.project.devede_project(config_data)
mwindow.ask_type()
Gtk.main()

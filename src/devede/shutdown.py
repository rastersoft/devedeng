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

from gi.repository import Gio, GLib

class shutdown:

    def __init__(self):

        # First, try with logind
        try:
            bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
            bus.call_sync("org.freedesktop.login1", "/org/freedesktop/login1", "org.freedesktop.login1.Manager",
                          "PowerOff", GLib.Variant_boolean('(bb)', ( False , False) ), None, Gio.DBusCallFlags.NONE, -1, None)
        except:
            failure=True

        if (failure):
            failure=False

            # If it fails, try with ConsoleKit
            try:
                bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
                bus.call_sync("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager", "org.freedesktop.ConsoleKit.Manager",
                              "Stop", None, None, Gio.DBusCallFlags.NONE, -1, None)
            except:
                failure=True

        if (failure):
            failure=False

            # If it fails, try with HAL
            try:
                bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
                bus.call_sync("org.freedesktop.Hal", "/org/freedesktop/Hal/devices/computer","org.freedesktop.Hal.Device.SystemPowerManagement",
                              "Shutdown", None, None, Gio.DBusCallFlags.NONE, -1, None)
            except:
                failure=True

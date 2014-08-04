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

import dbus

class shutdown:
    
    def __init__(self):

        # First, try with logind
        try:
            bus = dbus.SystemBus()
            bus_object = bus.get_object("org.freedesktop.login1", "/org/freedesktop/login1")
            bus_object.PowerOff(False, dbus_interface="org.freedesktop.login1.Manager")
        except:
            failure=True

        if (failure):
            failure=False
            
            # If it fails, try with ConsoleKit
            try:
                bus = dbus.SystemBus()
                bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
                bus_object.Stop(dbus_interface="org.freedesktop.ConsoleKit.Manager")
            except:
                failure=True

        if (failure):
            failure=False

            # If it fails, try with HAL
            try:
                bus = dbus.SystemBus()
                bus_object = bus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/devices/computer")
                bus_object.Shutdown(dbus_interface="org.freedesktop.Hal.Device.SystemPowerManagement")
            except:
                failure=True

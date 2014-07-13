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

        self.PAL = True
        self.tmp_folder = "/var/tmp"
        self.multicore = True
        self.final_folder = None
        self.sub_language = None
        self.sub_codepage = None

        config_path = os.path.join(os.environ.get("HOME"),".devede")
        try:
            config_data = open(config_path,"r")
            for linea in config_data:
                linea = linea.strip()
                if linea == "":
                    continue
                if linea[0] == "#":
                    continue
                if linea[:13]=="video_format:":
                    if linea[13:].strip() =="pal":
                        self.PAL=True
                        continue
                    if linea[13:].strip()=="ntsc":
                        self.PAL=False
                        continue
                if linea[:12]=="temp_folder:":
                    self.tmp_folder=linea[12:].strip()
                if linea[:10]=="multicore:":
                    if linea[10:].strip()=="1":
                        self.multicore = False
                    else:
                        self.multicore = True
                if linea[:13]=="final_folder:":
                    self.final_folder=linea[13:].strip()
                if linea[:13]=="sub_language:":
                    self.sub_language=linea[13:].strip()
                if linea[:13]=="sub_codepage:":
                    self.sub_codepage=linea[13:].strip()
            config_data.close()
        except:
            pass
                 
    def save_config(self):
        
        config_path = os.path.join(os.environ.get("HOME"),".devede")
        try:
            config_data = open(config_path,"w")
            config_data.write("video_format:")
            if (self.PAL):
                config_data.write("pal\n")
            else:
                config_data.write("ntsc\n")
            if (self.tmp_folder != None):
                config_data.write("temp_folder:"+str(self.tmp_folder)+"\n")
            config_data.write("multicore:")
            if (self.multicore):
                config_data.write("2\n")
            else:
                config_data.write("1\n")
            if (self.final_folder != None):
                config_data.write("final_folder:"+str(self.final_folder)+"\n")
            if (self.sub_language != None):
                config_data.write("sub_language:"+str(self.sub_language)+"\n")
            if (self.sub_codepage != None):
                config_data.write("sub_codepage:"+str(self.sub_codepage)+"\n")
            config_data.close()
        except:
            pass

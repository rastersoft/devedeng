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

from gi.repository import GObject
import os
import pkg_resources

class configuration(GObject.GObject):

    current_configuration = None
    __gsignals__ = {'disc_type': (GObject.SIGNAL_RUN_FIRST, None,(str,))}

    @staticmethod
    def get_config():
        if configuration.current_configuration == None:
            configuration.current_configuration = configuration()
            if (configuration.current_configuration.fill_config()):
                configuration.current_configuration = None
        return configuration.current_configuration

    def __init__(self):
        GObject.GObject.__init__(self)
        self.version = str(pkg_resources.require("devedeng")[0].version)
        print("Version: "+self.version)

    def fill_config(self):

        self.cores = 0
        proc_file = open("/proc/cpuinfo","r")
        for line in proc_file:
            if (line.startswith("processor")):
                self.cores += 1
        proc_file.close()

        is_local = None
        self.log = ""
        self.disc_type = None

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
            return True
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
        self.multicore = self.cores
        self.final_folder = os.environ.get("HOME")
        self.sub_language = None
        self.sub_codepage = None
        self.film_analizer = None
        self.film_player = None
        self.film_converter = None
        self.menu_converter = None
        self.subtitles_font_size = 28
        self.sub_language = None
        self.sub_codepage = None
        self.burner = None
        self.mkiso = None
        self.subt_fill_color = (1,1,1,1)
        self.subt_outline_color = (0,0,0,1)
        self.subt_outline_thickness = 0.0

        config_path = os.path.join(os.environ.get("HOME"),".devedeng")
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
                    elif linea[13:].strip()=="ntsc":
                        self.PAL=False
                    continue
                if linea[:12]=="temp_folder:":
                    self.tmp_folder=linea[12:].strip()
                    continue
                if linea[:10]=="multicore:":
                    self.multicore = int(linea[10:].strip())
                    continue
                if linea[:13]=="final_folder:":
                    self.final_folder=linea[13:].strip()
                    continue
                if linea[:13]=="sub_language:":
                    self.sub_language=linea[13:].strip()
                    continue
                if linea[:13]=="sub_codepage:":
                    self.sub_codepage=linea[13:].strip()
                    continue
                if linea[:14]=="film_analizer:":
                    self.film_analizer = linea[14:].strip()
                    continue
                if linea[:12]=="film_player:":
                    self.film_player = linea[12:].strip()
                    continue
                if linea[:15]=="film_converter:":
                    self.film_converter = linea[15:].strip()
                    continue
                if linea[:15]=="menu_converter:":
                    self.menu_converter = linea[15:].strip()
                    continue
                if linea[:7]=="burner:":
                    self.burner = linea[7:].strip()
                    continue
                if linea[:6]=="mkiso:":
                    self.mkiso = linea[6:].strip()
                    continue
                if linea[:19]=="subtitle_font_size:":
                    self.subtitles_font_size = int(linea[19:].strip())
                    continue
                if linea[:20] == "subtitle_fill_color:":
                    c = linea[20:].strip().split(",")
                    self.subt_fill_color = (float(c[0]), float(c[1]), float(c[2]), 1.0)
                if linea[:23] == "subtitle_outline_color:":
                    c = linea[23:].strip().split(",")
                    self.subt_outline_color = (float(c[0]), float(c[1]), float(c[2]), 1.0)
                if linea[:27] == "subtitle_outilne_thickness:":
                    self.subt_outline_thickness = float(linea[27:].strip())
            config_data.close()
        except:
            pass

        return False


    def set_disc_type(self,disc_type):

        self.disc_type = disc_type
        self.emit('disc_type',disc_type)


    def save_config(self):

        config_path = os.path.join(os.environ.get("HOME"),".devedeng")
        try:
            config_data = open(config_path,"w")
            config_data.write("video_format:")
            if (self.PAL):
                config_data.write("pal\n")
            else:
                config_data.write("ntsc\n")
            if (self.tmp_folder != None):
                config_data.write("temp_folder:"+str(self.tmp_folder)+"\n")
            config_data.write("multicore:"+str(self.multicore)+"\n")
            if (self.final_folder != None):
                config_data.write("final_folder:"+str(self.final_folder)+"\n")
            if (self.sub_language != None):
                config_data.write("sub_language:"+str(self.sub_language)+"\n")
            if (self.sub_codepage != None):
                config_data.write("sub_codepage:"+str(self.sub_codepage)+"\n")
            if (self.film_analizer != None):
                config_data.write("film_analizer:"+str(self.film_analizer)+"\n")
            if (self.film_player != None):
                config_data.write("film_player:"+str(self.film_player)+"\n")
            if (self.film_converter != None):
                config_data.write("film_converter:"+str(self.film_converter)+"\n")
            if (self.menu_converter != None):
                config_data.write("menu_converter:"+str(self.menu_converter)+"\n")
            if self.burner != None:
                config_data.write("burner:"+str(self.burner)+"\n")
            if self.mkiso != None:
                config_data.write("mkiso:"+str(self.mkiso)+"\n")
            if (self.sub_codepage != None):
                config_data.write("sub_codepage:"+str(self.sub_codepage)+"\n")
            if (self.sub_language != None):
                config_data.write("sub_language:"+str(self.sub_language)+"\n")
            config_data.write("subtitle_font_size:"+str(self.subtitles_font_size)+"\n")
            config_data.write("subtitle_fill_color:"+str(self.subt_fill_color[0])+","+str(self.subt_fill_color[1])+","+str(self.subt_fill_color[2])+"\n")
            config_data.write("subtitle_outline_color:"+str(self.subt_outline_color[0])+","+str(self.subt_outline_color[1])+","+str(self.subt_outline_color[2])+"\n")
            config_data.write("subtitle_outilne_thickness:"+str(self.subt_outline_thickness))

            config_data.close()
        except:
            pass


    def append_log(self,data,cr = True):

        self.log+=data
        if (cr):
            self.log += "\n"


    def clear_log(self):

        self.log = ""


    def get_log(self):

        return self.log

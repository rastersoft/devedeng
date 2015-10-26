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

from gi.repository import Gtk,GObject
import os
import subprocess

import devedeng.configuration_data

class choose_disc_type(GObject.GObject):

    def __init__(self):

        self.config  = devedeng.configuration_data.configuration.get_config()

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(self.config.glade,"wselect_disk.ui"))
        builder.connect_signals(self)
        self.wask_window = builder.get_object("wselect_disk")

        self.cv = devedeng.converter.converter.get_converter()
        dvd = True
        vcd = True
        cvd = True
        svcd = True
        divx = True
        mkv = True
        analizers, players, converters, menuers, burners, mkiso = self.cv.get_needed_programs()

        if (analizers != None) or (converters != None):
            dvd = False
            vcd = False
            cvd = False
            svcd = False
            divx = False
            mkv = False

        if menuers != None:
            dvd = False

        if mkiso != None:
            dvd = False

        if self.check_program(["dvdauthor","--help"]) == False:
            dvd = False
        if self.check_program(["vcdimager","--help"]) == False:
            vcd = False
            svcd = False
            cvd = False
        if self.check_program(["spumux" , "--help"]) == False:
            dvd = False
            vcd = False
            svcd = False
            cvd = False

        if self.cv.discs.count("dvd") == 0:
            dvd = False
        if self.cv.discs.count("vcd") == 0:
            vcd = False
        if self.cv.discs.count("svcd") == 0:
            svcd = False
        if self.cv.discs.count("cvd") == 0:
            cvd = False
        if self.cv.discs.count("divx") == 0:
            divx = False
        if self.cv.discs.count("mkv") == 0:
            mkv = False

        builder.get_object("button_dvd").set_sensitive(dvd)
        builder.get_object("button_vcd").set_sensitive(vcd)
        builder.get_object("button_svcd").set_sensitive(svcd)
        builder.get_object("button_cvd").set_sensitive(cvd)
        builder.get_object("button_divx").set_sensitive(divx)
        builder.get_object("button_mkv").set_sensitive(mkv)

        self.wask_window.show_all()

    def check_program(self,command_line):
        try:
            handle = subprocess.Popen(command_line, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            (stdout, stderr) = handle.communicate()
            retval = handle.wait()
            return True
        except:
            return False

    def set_type(self,disc_type):
        
        self.config.set_disc_type(disc_type)
        self.wask_window.hide()
        self.wask_window.destroy()
        self.wask_window = None

    def on_button_dvd_clicked(self,b):

        self.set_type("dvd")

    def on_button_vcd_clicked(self,b):

        self.set_type("vcd")

    def on_button_svcd_clicked(self,b):

        self.set_type("svcd")

    def on_button_cvd_clicked(self,b):

        self.set_type("cvd")

    def on_button_divx_clicked(self,b):

        self.set_type("divx")

    def on_button_mkv_clicked(self,b):

        self.set_type("mkv")

    def on_help_clicked(self,b):
        
        help_file = devedeng.help.help("select.html")

    def on_programs_needed_clicked(self,b):

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)
        builder.add_from_file(os.path.join(self.config.glade,"wneeded.ui"))
        window = builder.get_object("needed")
        textbuf = builder.get_object("textbuffer")

        window.show_all()

        analizers, players, menuers, converters, burners, mkiso = self.cv.get_supported_programs()
        analizers_i, players_i, menuers_i, converters_i, burners_i, mkiso_i = self.cv.get_available_programs()

        text = ""
        for e in analizers:
            if analizers_i.count(e.display_name) == 0:
                text += _("\t%(program_name)s (not installed)\n") % {"program_name": e.display_name}
            else:
                text += _("\t%(program_name)s (installed)\n") % {"program_name": e.display_name}
        text1 = _("Movie identifiers (install at least one of these):\n\n%(program_list)s\n") % {"program_list" : text}

        text = ""
        for e in players:
            if players_i.count(e.display_name) == 0:
                text += _("\t%(program_name)s (not installed)\n") % {"program_name": e.display_name}
            else:
                text += _("\t%(program_name)s (installed)\n") % {"program_name": e.display_name}
        text2 = _("Movie players (install at least one of these):\n\n%(program_list)s\n") % {"program_list" : text}

        text = ""
        for e in converters:
            sup = ""
            for s in e.disc_types:
                if sup != "":
                    sup += ", "
                sup += s
            if converters_i.count(e.display_name) == 0:
                text += _("\t%(program_name)s (not installed)\n") % {"program_name": e.display_name + " ("+sup+")"}
            else:
                text += _("\t%(program_name)s (installed)\n") % {"program_name": e.display_name + " ("+sup+")"}
        text3 = _("Movie Converters (install at least one of these):\n\n%(program_list)s\n") % {"program_list" : text}

        text = ""
        for e in burners:
            if burners_i.count(e.display_name) == 0:
                text += _("\t%(program_name)s (not installed)\n") % {"program_name": e.display_name}
            else:
                text += _("\t%(program_name)s (installed)\n") % {"program_name": e.display_name}
        text4 = _("CD/DVD burners (install at least one of these):\n\n%(program_list)s\n") % {"program_list" : text}

        text = ""
        for e in mkiso:
            if mkiso_i.count(e.display_name) == 0:
                text += _("\t%(program_name)s (not installed)\n") % {"program_name": e.display_name}
            else:
                text += _("\t%(program_name)s (installed)\n") % {"program_name": e.display_name}
        text5 = _("ISO creators (install at least one of these):\n\n%(program_list)s\n") % {"program_list" : text}

        text = ""
        if self.check_program(["dvdauthor","--help"]) == False:
            text += _("\t%(program_name)s (not installed)\n") % {"program_name": "DVDAUTHOR (dvd)"}
        else:
            text += _("\t%(program_name)s (installed)\n") % {"program_name":  "DVDAUTHOR (dvd)"}
        if self.check_program(["vcdimager","--help"]) == False:
            text += _("\t%(program_name)s (not installed)\n") % {"program_name": "VCDIMAGER (vcd, svcd, cvd)"}
        else:
            text += _("\t%(program_name)s (installed)\n") % {"program_name":  "VCDIMAGER (vcd, svcd, cvd)"}
        if self.check_program(["spumux" , "--help"]) == False:
            text += _("\t%(program_name)s (not installed)\n") % {"program_name": "SPUMUX (dvd, vcd, svcd, cvd)"}
        else:
            text += _("\t%(program_name)s (installed)\n") % {"program_name":  "SPUMUX (dvd, vcd, svcd, cvd)"}

        text6 = _("Other programs:\n\n%(program_list)s\n") % {"program_list" : text}

        final_text = text1+text2+text3+text4+text5+text6
        textbuf.insert_at_cursor(final_text,len(final_text))
        window.run()
        window.destroy()


    def on_wselect_disk_destroy_event(self,w,b):

        Gtk.main_quit()

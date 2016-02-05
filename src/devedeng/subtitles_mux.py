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
import subprocess

import devedeng.configuration_data
import devedeng.executor

class subtitles_mux(devedeng.executor.executor):

    def __init__(self):

        devedeng.executor.executor.__init__(self)
        self.config = devedeng.configuration_data.configuration.get_config()

    def multiplex_subtitles(self, file_path, subtitles_path, subt_codepage, subt_lang,
                            subt_upper, font_size, pal, force_subtitles, aspect, duration, stream_id, fill_color, outline_color, outline_thick):

        if len(fill_color) == 4:
            fill_color = fill_color[:3]
        if len(outline_color) == 4:
            outline_color = outline_color[:3]

        self.subt_path = file_path
        self.duration = duration
        self.text = _("Adding %(L)s subtitles to %(X)s") % {"X": os.path.basename(file_path), "L": subt_lang}

        out_xml = open(file_path+".xml","w")
        out_xml.write('<subpictures format="')
        if pal:
            out_xml.write('PAL')
        else:
            out_xml.write('NTSC')
        out_xml.write('">\n')
        out_xml.write('\t<stream>\n')
        out_xml.write('\t\t<textsub filename="')
        out_xml.write(self.expand_xml(subtitles_path))
        out_xml.write('" characterset="')
        out_xml.write(self.expand_xml(subt_codepage))
        out_xml.write('" fontsize="')
        out_xml.write(str(font_size))
        if subt_upper:
            out_xml.write('" bottom-margin="50')
        
        out_xml.write('" fill-color="#%02X%02X%02X"' % tuple([fill_color[i] * 255 for i in range(len(fill_color))]))
        out_xml.write(' outline-color="#%02X%02X%02X"' % tuple([outline_color[i] * 255 for i in range(len(outline_color))]))
        out_xml.write(' outline-thickness="%d"' % outline_thick)
        out_xml.write(' font="arial" horizontal-alignment="center" vertical-alignment="bottom" aspect="')
        out_xml.write(str(aspect))
        out_xml.write('" force="')
        if force_subtitles:
            out_xml.write('yes')
        else:
            out_xml.write('no')
        out_xml.write('" />\n')
        out_xml.write('\t</stream>\n')
        out_xml.write('</subpictures>')
        out_xml.close()
        
        self.command_var=[]
        self.command_var.append("spumux")
        mode = self.config.disc_type
        if mode == "vcd":
            mode = "svcd"
        self.command_var.append("-m")
        self.command_var.append(mode)
        self.command_var.append("-s")
        self.command_var.append(str(stream_id))
        self.command_var.append(file_path+".xml")
        self.stdin_file = file_path+".tmp"
        self.stdout_file = file_path


    def pre_function(self):

        final_path = self.subt_path+".tmp"
        if os.path.exists(final_path):
            os.remove(final_path)
        os.rename(self.subt_path, final_path)


    def process_stderr(self,data):

        if (data is None) or (len(data) == 0):
            return

        if self.duration == 0:
            return

        if data[0].startswith("STAT: "):
            time_pos = data[0][6:].split(":")
            current_time = 0
            for t in time_pos:
                current_time *= 60
                current_time += float(t)
            t = current_time / self.duration
            self.progress_bar[1].set_fraction(t)
            self.progress_bar[1].set_text("%.1f%%" % (100.0 * t))

        return

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

import subprocess
import devede.configuration_data

class mpv_converter:

    def __init__(self):

        self.config = devede.configuration_data.configuration.get_config()
        self.supports_analize = True
        self.supports_play = True
        self.supports_convert = False
        self.supports_menu = False
        self.display_name = "MPV"

    def check_is_installed(self):
        handle = subprocess.Popen(["mpv","-v"])
        if 0==handle.wait():
            return True
        else:
            return False

    def get_film_data(self,movie):
        """ processes a file, refered by the FILE_MOVIE movie object, and fills its
            main data (resolution, FPS, length...) """

    def get_film_data2(self,movie,check_audio):

        if (check_audio):
            frames = "0"
        else:
            frames = "1"

        if self.config.mpv_available:
            command_line = ["mpv","identify","-loop","1","-identify", "-ao", "null", "-vo", "null", "-frames", "1"]
        else:
            command_line = ["mplayer","identify","-loop","1","-identify", "-ao", "null", "-vo", "null", "-frames", "1"]

        command_line.append(movie.file_name)

        handle = subprocess.Popen(command_line)
        (stdout, stderr) = handle.communicate()

        minimum_audio=-1
        audio_list=[]
        audio = 0
        video = 0

        for line in stdout:
            line=self.remove_ansi(line)
            if line == "":
                continue
            position=line.find("ID_")
            if position==-1:
                continue
            line=line[position:]
            if line[:16]=="ID_VIDEO_BITRATE":
                vrate=int(line[17:])
            if line[:14]=="ID_VIDEO_WIDTH":
                width=int(line[15:])
            if line[:15]=="ID_VIDEO_HEIGHT":
                height=int(line[16:])
            if line[:15]=="ID_VIDEO_ASPECT":
                aspect_ratio=float(line[16:])
            if line[:12]=="ID_VIDEO_FPS":
                fps2=line[13:]
                while ord(fps2[-1])<32:
                    fps2=fps2[:-1]
                posic=line.find(".")
                if posic==-1:
                    fps=int(line[13:])
                else:
                    fps=int(line[13:posic])
                    if line[posic+1]=="9":
                        fps+=1
            if line[:16]=="ID_AUDIO_BITRATE":
                arate=int(line[17:])
            if line[:13]=="ID_AUDIO_RATE":
                audiorate=int(line[14:])
            if line[:9]=="ID_LENGTH":
                length=int(float(line[10:]))
            if line[:11]=="ID_VIDEO_ID":
                video+=1
            if line[:11]=="ID_AUDIO_ID":
                audio+=1
                audio_track=int(line[12:])
                if (minimum_audio == -1) or (minimum_audio>audio_track):
                    minimum_audio=audio_track
                audio_list.append(audio_track)
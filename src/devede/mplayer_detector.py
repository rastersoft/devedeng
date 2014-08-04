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

import subprocess
import devede.configuration_data
import devede.executor
import os

class mplayer_detector(devede.executor.executor):

    supports_analize = True
    supports_play = True
    supports_convert = False
    supports_menu = False
    supports_burn = False
    display_name = "MPLAYER"

    @staticmethod
    def check_is_installed():
        try:
            handle = subprocess.Popen(["mplayer","-v"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            (stdout, stderr) = handle.communicate()
            if 0==handle.wait():
                return True
            else:
                return False
        except:
            return False

    def __init__(self):

        devede.executor.executor.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()

    def play_film(self,file_name):

        command_line = ["mplayer", file_name]
        self.launch_process(command_line)

    def process_stdout(self,data):
        return

    def process_stderr(self,data):
        return

    def get_film_data(self, file_name):
        """ processes a file, refered by the FILE_MOVIE movie object, and fills its
            main data (resolution, FPS, length...) """

        self.original_file_size = os.path.getsize(file_name)
        (video, audio, length) = self.analize_film_data(file_name, True)

        if (video != 0):
            self.analize_film_data(file_name, False)
            return False # no error
        else:
            return True # the file is not a video file; maybe an audio-only file, or another thing

    def analize_film_data(self,file_name,check_audio):

        if (check_audio):
            frames = "0"
        else:
            frames = "1"

        command_line = ["mplayer","-loop","1","-identify", "-vo", "null", "-ao", "null", "-frames", frames , file_name]

        (stdout, stderr) = self.launch_process(command_line, False)

        minimum_audio=-1
        self.audio_list=[]
        self.audio_streams = 0
        self.video_streams = 0
        self.original_width = 0
        self.original_height = 0
        self.original_length = 0
        self.original_videorate = 0
        self.original_audiorate = 0
        self.original_audiorate_uncompressed = 0
        self.original_fps = 0
        self.original_aspect_ratio = 0

        try:
            stdout2 = stdout.decode("utf-8")
        except:
            stdout2 = stdout.decode("latin1")

        for line in stdout2.split("\n"):
            line=self.remove_ansi(line)
            if line == "":
                continue
            position=line.find("ID_")
            if position==-1:
                continue
            line=line[position:]

            if line[:16]=="ID_VIDEO_BITRATE":
                self.original_videorate=int(int(line[17:])/1000)
            if line[:14]=="ID_VIDEO_WIDTH":
                self.original_width=int(line[15:])
            if line[:15]=="ID_VIDEO_HEIGHT":
                self.original_height=int(line[16:])
            if line[:15]=="ID_VIDEO_ASPECT":
                self.original_aspect_ratio=float(line[16:])
            if line[:12]=="ID_VIDEO_FPS":
                self.original_fps=float(line[13:])
            if line[:16]=="ID_AUDIO_BITRATE":
                self.original_audiorate=int(int(line[17:])/1000)
            if line[:13]=="ID_AUDIO_RATE":
                self.original_audiorate_uncompressed=int(line[14:])
            if line[:9]=="ID_LENGTH":
                self.original_length=int(float(line[10:]))

            if line[:11]=="ID_VIDEO_ID":
                self.video_streams+=1
            if line[:11]=="ID_AUDIO_ID":
                self.audio_streams+=1
                audio_track=int(line[12:])
                if (minimum_audio == -1) or (minimum_audio>audio_track):
                    minimum_audio=audio_track
                self.audio_list.append(audio_track)

        if (check_audio):

            return (self.video_streams, self.audio_streams, self.original_length)

        else:

            self.original_size = str(self.original_width)+"x"+str(self.original_height)
            if (self.original_aspect_ratio == None) or (self.original_aspect_ratio <= 1.0):
                if (self.original_height != 0):
                    self.original_aspect_ratio = (float(self.original_width))/(float(self.original_height))

            if (self.original_aspect_ratio != None):
                self.original_aspect_ratio = (float(int(self.original_aspect_ratio*1000.0)))/1000.0

            if (self.video_streams == 0):
                return False
            else:
                return True
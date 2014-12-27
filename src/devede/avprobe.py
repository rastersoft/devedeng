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
import json

class avprobe(devede.executor.executor):

    supports_analize = True
    supports_play = False
    supports_convert = False
    supports_menu = False
    supports_mkiso = False
    supports_burn = False
    display_name = "AVPROBE"

    @staticmethod
    def check_is_installed():
        try:
            handle = subprocess.Popen(["avprobe","-h"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
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

    def process_stdout(self,data):
        return

    def process_stderr(self,data):
        return

    def get_division(self,data):
        pos = data.find("/")
        pos2 = data.find(":")

        if (pos == -1):
            pos = pos2

        if (pos == -1):
            return float(data)
        else:
            data1 = float(data[:pos])
            data2 = float(data[pos+1:])
            if (data2 == 0):
                return 0
            else:
                return data1 / data2

    def get_film_data(self, file_name):
        """ processes a file, refered by the FILE_MOVIE movie object, and fills its
            main data (resolution, FPS, length...) """

        self.audio_list=[]
        self.audio_streams = 0
        self.video_list=[]
        self.video_streams = 0
        self.original_width = 0
        self.original_height = 0
        self.original_length = 0
        self.original_videorate = 0
        self.original_audiorate = 0
        self.original_audiorate_uncompressed = 0
        self.original_fps = 0
        self.original_aspect_ratio = 0

        self.original_file_size = os.path.getsize(file_name)

        command_line = ["avprobe",file_name,"-print_format","json","-show_streams", "-loglevel", "quiet"]

        (stdout, stderr) = self.launch_process(command_line, False)
        try:
            stdout2 = stdout.decode("utf-8")
        except:
            stdout2 = stdout.decode("latin1")

        try:
            video_data = json.loads(stdout2)
        except:
            return True # There was an error reading the JSON data

        for element in video_data["streams"]:
            if (element["codec_type"]=="video"):
                self.video_streams += 1
                self.video_list.append(element["index"])
                if (self.video_streams == 1):
                    self.original_width = int(float(element["width"]))
                    self.original_height = int(float(element["height"]))
                    self.original_length = int(float(element["duration"]))
                    self.original_videorate = int(float(element["bit_rate"]))/1000
                    self.original_fps = self.get_division(element["avg_frame_rate"])
                    self.original_aspect_ratio = self.get_division(element["display_aspect_ratio"])
            elif (element["codec_type"]=="audio"):
                self.audio_streams += 1
                self.audio_list.append(element["index"])
                if (self.audio_streams == 1):
                    self.original_audiorate = int(float(element["bit_rate"]))/1000
                    self.original_audiorate_uncompressed = int(float(element["sample_rate"]))

        self.original_size = str(self.original_width)+"x"+str(self.original_height)
        if (self.original_aspect_ratio == None) or (self.original_aspect_ratio <= 1.0):
            if (self.original_height != 0):
                self.original_aspect_ratio = (float(self.original_width))/(float(self.original_height))

        if (self.original_aspect_ratio != None):
            self.original_aspect_ratio = (float(int(self.original_aspect_ratio*1000.0)))/1000.0

        if (len(self.video_list) == 0):
            return True # the file is not a video file; maybe an audio-only file or another thing

        return False # no error

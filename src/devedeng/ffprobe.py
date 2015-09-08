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
import devedeng.configuration_data
import devedeng.executor
import os
import json

class ffprobe(devedeng.executor.executor):

    supports_analize = True
    supports_play = False
    supports_convert = False
    supports_menu = False
    supports_mkiso = False
    supports_burn = False
    display_name = "FFPROBE"

    @staticmethod
    def check_is_installed():
        try:
            handle = subprocess.Popen(["ffprobe","-h"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            (stdout, stderr) = handle.communicate()
            if 0==handle.wait():
                return True
            else:
                return False
        except:
            return False

    def __init__(self):

        devedeng.executor.executor.__init__(self)
        self.config = devedeng.configuration_data.configuration.get_config()

    def process_stdout(self,data):
        return

    def process_stderr(self,data):
        return

    def get_film_data(self, file_name):
        """ processes a file, refered by the FILE_MOVIE movie object, and fills its
            main data (resolution, FPS, length...) """

        self.original_file_size = os.path.getsize(file_name)

        command_line = ["ffprobe",file_name,"-of","json","-show_streams", "-loglevel", "quiet"]

        (stdout, stderr) = self.launch_process(command_line, False)
        try:
            stdout2 = stdout.decode("utf-8")
        except:
            stdout2 = stdout.decode("latin1")

        self.config.append_log("FFProbe JSON data: "+str(stdout2))
        return self.process_json(file_name,stdout2)


    def process_json(self,file_name,stdout2):

        self.audio_list=[]
        self.audio_streams = 0
        self.video_list=[]
        self.video_streams = 0
        self.original_width = 0
        self.original_height = 0
        self.original_length = -1
        self.original_videorate = 0
        self.original_audiorate = 0
        self.original_audiorate_uncompressed = 0
        self.original_fps = 0
        self.original_aspect_ratio = 0

        try:
            video_data = json.loads(stdout2)
        except:
            return True # There was an error reading the JSON data

        if not("streams" in video_data):
            return True # There are no streams!!!!!

        for element in video_data["streams"]:

            if (self.original_length == -1) and ("duration" in element):
                try:
                    self.original_length = int(float(element["duration"]))
                except:
                    self.original_length = -1

            if (element["codec_type"]=="video"):
                self.video_streams += 1
                self.video_list.append(element["index"])
                if (self.video_streams == 1):
                    self.original_width = int(float(element["width"]))
                    self.original_height = int(float(element["height"]))
                    if ("bit_rate" in element):
                        self.original_videorate = int(float(element["bit_rate"]))/1000
                    self.original_fps = self.get_division(element["avg_frame_rate"])
                    if ("display_aspect_ratio" in element):
                        self.original_aspect_ratio = self.get_division(element["display_aspect_ratio"])

            elif (element["codec_type"]=="audio"):
                self.audio_streams += 1
                self.audio_list.append(element["index"])
                if (self.audio_streams == 1):
                    if ("bit_rate" in element):
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

        if self.original_length == -1: # if it was unable to detect the duration, try to use the human readable format
            command_line = ["ffprobe",file_name]
            (stdout, stderr) = self.launch_process(command_line, False)
            try:
                stdout2 = stdout.decode("utf-8") + "\n" + stderr.decode("utf-8")
            except:
                stdout2 = stdout.decode("latin1") + "\n" + stderr.decode("latin1")
            self.config.append_log("Using ffprobe human readable format: "+str(stdout2))
            for line in stdout2.split("\n"):
                line = line.strip()
                if line.startswith("Duration: "):
                    self.original_length = self.get_time(line[10:])
                    break

        return False # no error

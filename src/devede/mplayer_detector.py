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

class mplayer_detector:

    supports_analize = True
    supports_play = True
    supports_convert = False
    supports_menu = False
    display_name = "MPLAYER"

    @staticmethod
    def check_is_installed():
        handle = subprocess.Popen(["mplayer","-v"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        (stdout, stderr) = handle.communicate()
        if 0==handle.wait():
            return True
        else:
            return False

    def __init__(self):

        self.config = devede.configuration_data.configuration.get_config()

    def get_film_data(self,movie):
        """ processes a file, refered by the FILE_MOVIE movie object, and fills its
            main data (resolution, FPS, length...) """

        video = self.get_film_data2(movie, True)

        if (video):
            self.get_film_data2(movie, False)
            return False # no error
        else:
            return True # the file is not a video file; maybe an audio-only file, or another thing

    def get_film_data2(self,movie,check_audio):

        if (check_audio):
            frames = "0"
        else:
            frames = "1"

        command_line = ["mplayer","-loop","1","-identify", "-vo", "null", "-ao", "null", "-frames", frames , movie.file_name]

        handle = subprocess.Popen(command_line, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        (stdout, stderr) = handle.communicate()

        minimum_audio=-1
        movie.audio_list=[]
        movie.audio_streams = 0
        movie.video_streams = 0
        movie.original_width = 0
        movie.original_height = 0

        for line in str(stdout).split("\\n"):
            #line=self.remove_ansi(line)
            if line == "":
                continue
            position=line.find("ID_")
            if position==-1:
                continue
            line=line[position:]
            if (not check_audio):
                if line[:16]=="ID_VIDEO_BITRATE":
                    movie.original_videorate=int(int(line[17:])/1000)
                if line[:14]=="ID_VIDEO_WIDTH":
                    movie.original_width=int(line[15:])
                if line[:15]=="ID_VIDEO_HEIGHT":
                    movie.original_height=int(line[16:])
                if line[:15]=="ID_VIDEO_ASPECT":
                    movie.original_aspect_ratio=float(line[16:])
                if line[:12]=="ID_VIDEO_FPS":
                    movie.original_fps=float(line[13:])
                if line[:16]=="ID_AUDIO_BITRATE":
                    movie.original_audiorate=int(int(line[17:])/1000)
                if line[:13]=="ID_AUDIO_RATE":
                    movie.original_audiorate_uncompressed=int(line[14:])
                if line[:9]=="ID_LENGTH":
                    movie.original_length=int(float(line[10:]))

            if line[:11]=="ID_VIDEO_ID":
                movie.video_streams+=1
            if line[:11]=="ID_AUDIO_ID":
                movie.audio_streams+=1
                audio_track=int(line[12:])
                if (minimum_audio == -1) or (minimum_audio>audio_track):
                    minimum_audio=audio_track
                movie.audio_list.append(audio_track)

        movie.original_size = str(movie.original_width)+"x"+str(movie.original_height)
        if (movie.original_aspect_ratio == None) or (movie.original_aspect_ratio <= 1.0):
            if (movie.original_height != 0):
                movie.original_aspect_ratio = (float(movie.original_width))/(float(movie.original_height))

        if (movie.original_aspect_ratio != None):
            movie.original_aspect_ratio = (float(int(movie.original_aspect_ratio*1000.0)))/1000.0

        if (movie.video_streams == 0):
            return False
        else:
            return True
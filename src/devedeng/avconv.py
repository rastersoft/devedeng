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
import os
import devedeng.configuration_data
import devedeng.avbase
import devedeng.mux_dvd_menu

class avconv(devedeng.avbase.avbase):

    supports_analize = False
    supports_play = False
    supports_convert = True
    supports_menu = True
    supports_mkiso = False
    supports_burn = False
    display_name = "AVCONV"
    disc_types = []


    @staticmethod
    def check_is_installed():
        try:
            handle = subprocess.Popen(["avconv","-codecs"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            (stdout, stderr) = handle.communicate()
            if 0==handle.wait():
                mp2 = False
                mp3 = False
                ac3 = False
                mpeg1 = False
                mpeg2 = False
                divx = False
                h264 = False
                for line in stdout.decode("latin-1").split("\n"):
                    parts = line.strip().split(" ")
                    if len(parts) < 2:
                        continue
                    if len(parts[0]) != 6:
                        continue
                    capabilities = parts[0]
                    codec = parts[1]

                    if capabilities[1] != 'E':
                        continue

                    if (codec == "mpeg1video"):
                        mpeg1 = True
                        continue
                    if (codec == "mpeg2video"):
                        mpeg2 = True
                        continue
                    if (codec == "mp2"):
                        mp2 = True
                        continue
                    if (codec == "mp3"):
                        mp3 = True
                        continue
                    if (codec == "ac3"):
                        ac3 = True
                        continue
                    if (codec == "h264") or (codec == "H264"):
                        h264 = True
                        continue
                    if (codec == "mpeg4"):
                        divx = True
                        continue

                if (mpeg1 and mp2):
                    devedeng.avconv.avconv.disc_types.append("vcd")
                if (mpeg2 and mp2):
                    devedeng.avconv.avconv.disc_types.append("svcd")
                    devedeng.avconv.avconv.disc_types.append("cvd")
                if (mpeg2 and mp2 and ac3):
                    devedeng.avconv.avconv.disc_types.append("dvd")
                if (divx and mp3):
                    devedeng.avconv.avconv.disc_types.append("divx")
                if (h264 and mp3):
                    devedeng.avconv.avconv.disc_types.append("mkv")

                return True
            else:
                return False
        except:
            return False


    def __init__(self):

        devedeng.executor.executor.__init__(self)
        self.config = devedeng.configuration_data.configuration.get_config()
        self.check_version(["avconv","-version"])


    def convert_file(self,file_project,output_file,video_length,pass2 = False):

        if file_project.two_pass_encoding:
            if pass2:
                self.text = _("Converting %(X)s (pass 2)") % {"X" : file_project.title_name}
            else:
                self.text = _("Converting %(X)s (pass 1)") % {"X" : file_project.title_name}
                # Prepare the converting process for the second pass
                tmp = devedeng.avconv.avconv()
                tmp.convert_file(file_project, output_file, video_length, True)
                # it deppends of this process
                tmp.add_dependency(self)
                # add it as a child process of this one
                self.add_child_process(tmp)
        else:
            self.text = _("Converting %(X)s") % {"X" : file_project.title_name}

        if (pass2 == False) and (file_project.two_pass_encoding == True):
            # this is the first pass in a 2-pass codification
            second_pass = False
        else:
            # second_pass is TRUE in the second pass of a 2-pass codification, and also when not doing 2-pass codification
            # It is used to remove unnecessary steps during the first pass, but that are needed on the second pass, or when not using 2-pass codification 
            second_pass = True

        if (video_length == 0):
            self.final_length = file_project.original_length
        else:
            self.final_length = video_length
        self.command_var=[]
        self.command_var.append("avconv")
        self.command_var.append("-i")
        self.command_var.append(file_project.file_name)

        if (file_project.volume!=100) and second_pass:
            self.command_var.append("-vol")
            self.command_var.append(str((256*file_project.volume)/100))

        if (file_project.audio_delay != 0.0) and (file_project.copy_sound==False) and (file_project.no_reencode_audio_video==False) and second_pass:
            self.command_var.append("-itsoffset")
            self.command_var.append(str(file_project.audio_delay))

        self.command_var.append("-i")
        self.command_var.append(file_project.file_name)
        self.command_var.append("-map")
        self.command_var.append("1:"+str(file_project.video_list[0]))
        if (not file_project.copy_sound) and (not file_project.no_reencode_audio_video):
            for l in file_project.audio_list:
                self.command_var.append("-map")
                self.command_var.append("0:"+str(l))

        if (file_project.no_reencode_audio_video==False) and second_pass:
            cmd_line=""

            if file_project.deinterlace=="deinterlace_yadif":
                cmd_line+="yadif"

            vflip=False
            hflip=False

            if (file_project.rotation=="rotation_90"):
                if (cmd_line!=""):
                    cmd_line+=",fifo,"
                cmd_line+="transpose=1"
            elif (file_project.rotation=="rotation_270"):
                if (cmd_line!=""):
                    cmd_line+=",fifo,"
                cmd_line+="transpose=2"
            elif (file_project.rotation=="rotation_180"):
                vflip=True
                hflip=True

            if (file_project.mirror_vertical):
                vflip=not vflip
            if (file_project.mirror_horizontal):
                hflip=not hflip

            if (vflip):
                if (cmd_line!=""):
                    cmd_line+=",fifo,"
                cmd_line+="vflip"
            if (hflip):
                if (cmd_line!=""):
                    cmd_line+=",fifo,"
                cmd_line+="hflip"

            if (file_project.width_midle != file_project.original_width) or (file_project.height_midle != file_project.original_height):
                if (cmd_line!=""):
                    cmd_line+=",fifo,"
                x = int((file_project.width_midle - file_project.original_width) /2)
                y = int((file_project.height_midle - file_project.original_height) /2)
                if (x > 0) or (y > 0):
                    cmd_line+="pad="+str(file_project.width_midle)+":"+str(file_project.height_midle)+":"+str(x)+":"+str(y)+":0x000000"
                else:
                    cmd_line+="crop="+str(file_project.width_midle)+":"+str(file_project.height_midle)+":"+str(x)+":"+str(y)

            if (file_project.width_final != file_project.width_midle) or (file_project.height_final != file_project.height_midle):
                if (cmd_line!=""):
                    cmd_line+=",fifo,"
                if self.major_version < 11:
                    cmd_line+="scale="+str(file_project.width_final)+":"+str(file_project.height_final)
                else:
                    cmd_line+="scale=w="+str(file_project.width_final)+":h="+str(file_project.height_final)

            if cmd_line!="":
                self.command_var.append("-vf")
                self.command_var.append(cmd_line)


        self.command_var.append("-y")

        vcd=False

        if (self.config.disc_type == "divx"):
            self.command_var.append("-vcodec")
            self.command_var.append("mpeg4")
            self.command_var.append("-acodec")
            self.command_var.append("libmp3lame")
            self.command_var.append("-f")
            self.command_var.append("avi")
        elif (self.config.disc_type == "mkv"):
            self.command_var.append("-vcodec")
            self.command_var.append("h264")
            self.command_var.append("-acodec")
            self.command_var.append("libmp3lame")
            self.command_var.append("-f")
            self.command_var.append("matroska")
        else:
            self.command_var.append("-target")
            if (self.config.disc_type=="dvd"):
                if not file_project.format_pal:
                    self.command_var.append("ntsc-dvd")
                elif (file_project.original_fps==24):
                    self.command_var.append("film-dvd")
                else:
                    self.command_var.append("pal-dvd")
                if (not file_project.copy_sound):
                    if file_project.sound5_1:
                        self.command_var.append("-acodec")
                        self.command_var.append("ac3")
            elif (self.config.disc_type=="vcd"):
                vcd=True
                if not file_project.format_pal:
                    self.command_var.append("ntsc-vcd")
                else:
                    self.command_var.append("pal-vcd")
            elif (self.config.disc_type=="svcd"):
                if not file_project.format_pal:
                    self.command_var.append("ntsc-svcd")
                else:
                    self.command_var.append("pal-svcd")
            elif (self.config.disc_type=="cvd"):
                if not file_project.format_pal:
                    self.command_var.append("ntsc-svcd")
                else:
                    self.command_var.append("pal-svcd")

        if  (not file_project.no_reencode_audio_video):
            self.command_var.append("-sn") # no subtitles

        if file_project.copy_sound or file_project.no_reencode_audio_video:
            self.command_var.append("-acodec")
            self.command_var.append("copy")

        if file_project.no_reencode_audio_video:
            self.command_var.append("-vcodec")
            self.command_var.append("copy")

        if (vcd==False):
            if not file_project.format_pal:
                if (file_project.original_fps==24) and ((self.config.disc_type=="dvd")):
                    keyintv=15
                else:
                    keyintv=18
            else:
                keyintv=15

            if not file_project.gop12:
                self.command_var.append("-g")
                self.command_var.append(str(keyintv))

        if (self.config.disc_type=="divx") or (self.config.disc_type=="mkv"):
            self.command_var.append("-g")
            self.command_var.append("300")
        elif file_project.gop12 and (file_project.no_reencode_audio_video==False):
            self.command_var.append("-g")
            self.command_var.append("12")

        self.command_var.append("-bf")
        self.command_var.append("2")
        self.command_var.append("-strict")
        self.command_var.append("1")

        if video_length != 0:
            self.command_var.append("-t")
            self.command_var.append(str(video_length))

        self.command_var.append("-ac")
        if (file_project.sound5_1) and ((self.config.disc_type=="dvd") or (self.config.disc_type=="divx") or (self.config.disc_type=="mkv")):
            self.command_var.append("6")
        else:
            self.command_var.append("2")

        self.command_var.append("-aspect")
        self.command_var.append(str(file_project.aspect_ratio_final))

        if self.config.disc_type=="divx":
            self.command_var.append("-vtag")
            self.command_var.append("DX50")

        if (file_project.deinterlace == "deinterlace_ffmpeg") and (file_project.no_reencode_audio_video==False) and second_pass:
            self.command_var.append("-deinterlace")

        if (file_project.no_reencode_audio_video==False) and (vcd==False) and second_pass:
            self.command_var.append("-s")
            self.command_var.append(str(file_project.width_final)+"x"+str(file_project.height_final))

        if second_pass:
            self.command_var.append("-trellis")
            self.command_var.append("1")
            self.command_var.append("-mbd")
            self.command_var.append("2")
        else:
            self.command_var.append("-trellis")
            self.command_var.append("0")
            self.command_var.append("-mbd")
            self.command_var.append("0")

        if (vcd == False) and (file_project.no_reencode_audio_video == False):
            self.command_var.append("-b:a")
            self.command_var.append(str(file_project.audio_rate_final)+"k")

            self.command_var.append("-b:v")
            self.command_var.append(str(file_project.video_rate_final)+"k")

        if file_project.two_pass_encoding == True:
            self.command_var.append("-passlogfile")
            self.command_var.append(output_file)
            self.command_var.append("-pass")
            if pass2:
                self.command_var.append("2")
            else:
                self.command_var.append("1")

        self.command_var.append(output_file)


    def create_menu_mpeg(self,n_page,background_music,sound_length,pal,video_rate, audio_rate,output_path, use_mp2):

        self.n_page = n_page
        self.final_length = float(sound_length)
        self.text = _("Creating menu %(X)d") % {"X": self.n_page}

        self.command_var=[]
        self.command_var.append("avconv")

        self.command_var.append("-loop")
        self.command_var.append("1")

        self.command_var.append("-f")
        self.command_var.append("image2")
        self.command_var.append("-i")
        self.command_var.append(os.path.join(output_path,"menu_"+str(n_page)+"_bg.png"))
        self.command_var.append("-i")
        self.command_var.append(background_music)

        self.command_var.append("-y")
        self.command_var.append("-target")
        if pal:
            self.command_var.append("pal-dvd")
        else:
            self.command_var.append("ntsc-dvd")
        self.command_var.append("-acodec")
        if (use_mp2):
            self.command_var.append("mp2")
            if (audio_rate > 384):
                audio_rate = 384 #max bitrate for mp2
        else:
            self.command_var.append("ac3")
        self.command_var.append("-s")
        if pal:
            self.command_var.append("720x576")
        else:
            self.command_var.append("720x480")
        self.command_var.append("-g")
        self.command_var.append("12")
        self.command_var.append("-b:v")
        self.command_var.append(str(video_rate)+"k")
        self.command_var.append("-b:a")
        self.command_var.append(str(audio_rate)+"k")
        self.command_var.append("-aspect")
        self.command_var.append("4:3")

        self.command_var.append("-t")
        self.command_var.append(str(1+sound_length))

        movie_path = os.path.join(output_path,"menu_"+str(n_page)+".mpg")
        self.command_var.append(movie_path)

        muxer = devedeng.mux_dvd_menu.mux_dvd_menu()
        final_path = muxer.create_mpg(n_page,output_path,movie_path)
        # the muxer process depends of the converter process
        muxer.add_dependency(self)
        self.add_child_process(muxer)

        return (final_path)

    def process_stdout(self,data):

        return

    def process_stderr(self,data):

        pos = data[0].find("time=")
        if (pos != -1):
            pos+=5
            pos2 = data[0].find(" ",pos)
            if (pos2 != -1):
                parts = data[0][pos:pos2].split(":")
                t = 0.0
                for e in parts:
                    t *= 60.0
                    t += float(e)
                t /= self.final_length
                self.progress_bar[1].set_fraction(t)
                self.progress_bar[1].set_text("%.1f%%" % (100.0 * t))
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
import devede.configuration_data
import devede.executor
import devede.mux_dvd_menu

class avconv_converter(devede.executor.executor):

    supports_analize = False
    supports_play = False
    supports_convert = True
    supports_menu = True
    display_name = "AVCONV"
    disc_types = ["dvd","vcd","svcd","cvd","divx","mkv"]

    @staticmethod
    def check_is_installed():
        handle = subprocess.Popen(["avconv","-version"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        (stdout, stderr) = handle.communicate()
        if 0==handle.wait():
            return True
        else:
            return False

    def __init__(self):

        devede.executor.executor.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()

    def convert_file(self,file_project,output_file,video_length):
        
        self.text = _("Converting %(X)s") % {"X" : file_project.title_name}
        
        self.final_length = file_project.original_length
        self.command_var=[]
        self.command_var.append("avconv")
        self.command_var.append("-i")
        self.command_var.append(file_project.file_name)
        
        if (file_project.volume!=100):
            self.command_var.append("-vol")
            self.command_var.append(str((256*file_project.volume)/100))
        
        if (file_project.audio_delay != 0.0) and (file_project.copy_sound==False) and (file_project.no_reencode_audio_video==False):
            self.command_var.append("-itsoffset")
            self.command_var.append(str(file_project.audio_delay))

        self.command_var.append("-i")
        self.command_var.append(file_project.file_name)
        self.command_var.append("-map")
        self.command_var.append("1:0")
        if (not file_project.copy_sound) and (not file_project.no_reencode_audio_video):
            for l in range (file_project.audio_streams):
                self.command_var.append("-map")
                self.command_var.append("0"+":"+str(l+1))

        if (file_project.no_reencode_audio_video==False):
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
            
#             if addbars and ((resx_inter!=resx_original) or (resy_inter!=resy_original)) and (default_res==False):
#                 if (cmd_line!=""):
#                     cmd_line+=",fifo,"
#                 cmd_line+="scale="+str(resx_inter)+":"+str(resy_inter)+",fifo,pad="+str(resx_final)+":"+str(resy_final)+":"+str(addx)+":"+str(addy)+":0x000000"
            
            if cmd_line!="":
                self.command_var.append("-vf")
                self.command_var.append(cmd_line)
            
        
        self.command_var.append("-y")

        vcd=False
        
        if (self.config.disc_type!="divx"):
            self.command_var.append("-target")
            if (self.config.disc_type=="dvd"):
                if not file_project.format_pal:
                    self.command_var.append("ntsc-dvd")
                elif (file_project.original_fps==24):
                    self.command_var.append("film-dvd")
                else:
                    self.command_var.append("pal-dvd")
                if (not file_project.copy_sound):
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
        else: # DivX
            self.command_var.append("-vcodec")
            self.command_var.append("mpeg4")
            self.command_var.append("-acodec")
            self.command_var.append("libmp3lame")
            self.command_var.append("-f")
            self.command_var.append("avi")
        
        if  (not file_project.no_reencode_audio_video):
            self.command_var.append("-sn") # no subtitles

        if file_project.copy_sound or file_project.no_reencode_audio_video:
            self.command_var.append("-acodec")
            self.command_var.append("copy")
        #else:
        #    if (self.config.disc_type=="divx"):
        #        self.command_var.append("-acodec")
        #        self.command_var.append("mp3")

        #if (audiostream!=10000):
        #    self.command_var.append("-aid")
        #    self.command_var.append(str(audiostream))

        if file_project.no_reencode_audio_video:
            self.command_var.append("-vcodec")
            self.command_var.append("copy")
        
        if (vcd==False):
            if not file_project.format_pal:
                if (file_project.original_fps==24) and ((self.config.disc_type=="dvd") or (self.config.disc_type=="divx")):
                    str_final_framerate="24000/1001"
                    keyintv=15
                    telecine=True
                else:
                    str_final_framerate="30000/1001"
                    keyintv=18
            else:
                str_final_framerate="25"
                keyintv=15
            if not file_project.gop12:
                self.command_var.append("-g")
                self.command_var.append(str(keyintv))

        if (self.config.disc_type=="divx"):
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
#         else:
#             if videofile["cutting"]==1: # first half only
#                 self.command_var.append("-t")
#                 self.command_var.append(str(videofile["olength"]/2))
#             elif videofile["cutting"]==2: # second half only
#                 self.command_var.append("-ss")
#                 self.command_var.append(str((videofile["olength"]/2)-5)) # start 5 seconds before

        #if (audiodelay!=0.0) and (copy_audio==False) and (isvob==False):
        #    self.command_var.append("-delay")
        #    self.command_var.append(str(audiodelay))

        self.command_var.append("-ac")
        if (file_project.sound5_1) and ((self.config.disc_type=="dvd") or (self.config.disc_type=="divx")):
            self.command_var.append("6")
        else:
            self.command_var.append("2")

        #if (isvob==False) and (default_res==False):
        #    self.command_var.append("-ofps")
        #    self.command_var.append(str_final_framerate)

        if self.config.disc_type=="divx":
            self.command_var.append("-vtag")
            self.command_var.append("DX50")

        if (file_project.deinterlace == "deinterlace_ffmpeg") and (file_project.no_reencode_audio_video==False):
            self.command_var.append("-deinterlace")
        
        if (file_project.no_reencode_audio_video==False) and (vcd==False):
            self.command_var.append("-s")
            self.command_var.append(str(file_project.width_final)+"x"+str(file_project.height_final))
        
        self.command_var.append("-trellis")
        self.command_var.append("1")
        
        self.command_var.append("-mbd")
        self.command_var.append("2")
        
        if (vcd == False) and (file_project.no_reencode_audio_video == False):
            self.command_var.append("-b:a")
            self.command_var.append(str(file_project.audio_rate_final)+"k")
        
            self.command_var.append("-b:v")
            self.command_var.append(str(file_project.video_rate_final)+"k")

        self.command_var.append(output_file)
        


    def create_menu_mpeg(self,n_page,background_music,sound_length,pal,output_path):

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
        self.command_var.append("mp2")
        self.command_var.append("-s")
        if pal:
            self.command_var.append("720x576")
        else:
            self.command_var.append("720x480")
        self.command_var.append("-g")
        self.command_var.append("12")
        self.command_var.append("-b:v")
        self.command_var.append("2500k")
        self.command_var.append("-b:a")
        self.command_var.append("192k")
        self.command_var.append("-aspect")
        self.command_var.append("4:3")

        self.command_var.append("-t")
        self.command_var.append(str(1+sound_length))

        self.command_var.append(os.path.join(output_path,"menu_"+str(n_page)+".mpg"))
        
        muxer = devede.mux_dvd_menu.mux_dvd_menu()
        muxer.create_mpg(n_page,output_path)
        # the muxer process depends of the converter process
        muxer.add_dependency(self)
        self.add_child_process(muxer)

    def process_stdout(self,data):

        pass

    def process_stderr(self,data):

        pos = data[0].find("time=")
        if (pos != -1):
            pos+=5
            pos2 = data[0].find(" ",pos)
            if (pos2 != -1):
                t = float(data[0][pos:pos2])
                self.progress_bar[1].set_fraction(t / self.final_length)
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

import devede.configuration_data
import devede.interface_manager
import devede.converter
import devede.ask_subtitles

class file_movie(devede.interface_manager.interface_manager):

    __gsignals__ = {'title_changed': (GObject.SIGNAL_RUN_FIRST, None,(str,))}

    def __init__(self,file_name):

        devede.interface_manager.interface_manager.__init__(self)

        self.wfile_properties = None
        self.builder = None

        self.config = devede.configuration_data.configuration.get_config()
        self.set_type(None, self.config.disc_type)
        self.config.connect('disc_type',self.set_type)

        self.add_text("file_name", file_name)
        self.add_text("title_name", os.path.splitext(os.path.basename(file_name))[0])
        self.add_label("original_size",None)
        self.add_label("original_length",None)
        self.add_label("original_videorate",None)
        self.add_label("original_audiorate",None)
        self.add_label("original_aspect_ratio",None)
        self.add_label("original_fps",None)

        self.add_toggle("show_in_menu", True)
        self.add_toggle("format_pal",self.config.PAL)
        self.add_toggle("video_rate_automatic", True)
        self.add_toggle("audio_rate_automatic", True)
        self.add_toggle("divide_in_chapters", True)
        self.add_toggle("force_subtitles", False)
        self.add_toggle("mirror_horizontal", False)
        self.add_toggle("mirror_vertical", False)
        self.add_toggle("two_pass_encoding", True)
        self.add_toggle("sound5_1", False)
        self.add_toggle("copy_sound", False)
        self.add_toggle("is_mpeg_ps", False)
        self.add_toggle("no_reencode_audio_video", False)
        if (self.disc_type == "divx") or (self.disc_type == "mkv"):
            self.add_toggle("gop12", False)
        else:
            self.add_toggle("gop12", True)

        self.add_group("final_size_pal", ["size_auto", "size_1920x1080", "size_1280x720", "size_720x576", "size_704x576", "size_480x576","size_352x576", "size_352x288"], "size_auto")
        self.add_group("final_size_ntsc", ["size_auto_ntsc", "size_1920x1080_ntsc", "size_1280x720_ntsc", "size_720x480_ntsc", "size_704x480_ntsc", "size_480x480_ntsc","size_352x480_ntsc", "size_352x240_ntsc"], "size_auto_ntsc")
        self.add_group("aspect_ratio", ["aspect_auto", "aspect_classic", "aspect_wide"], "aspect_auto")
        self.add_group("scaling", ["add_black_bars", "scale_picture" ,"cut_picture"], "add_black_bars")
        self.add_group("rotation",["rotation_0","rotation_90","rotation_180","rotation_270"], "rotation_0")
        self.add_group("deinterlace", ["deinterlace_none", "deinterlace_ffmpeg", "deinterlace_yadif"], "deinterlace_none")
        self.add_group("actions", ["action_stop","action_play_first","action__play_previous","action_play_again","action_play_next","action_play_last"], "action_stop")

        self.add_integer_adjustment("volume", 100)
        if (self.disc_type == "dvd"):
            self.add_integer_adjustment("video_rate", 5000)
        elif (self.disc_type == "vcd"):
            self.add_integer_adjustment("video_rate", 1152)
        else:
            self.add_integer_adjustment("video_rate", 2000)
        self.add_integer_adjustment("audio_rate", 224)
        self.add_integer_adjustment("subt_font_size", 28)
        self.add_float_adjustment("audio_delay", 0.0)

        self.add_list("subtitles_list")

        self.add_show_hide("format_pal", ["size_pal"], ["size_ntsc"])

        self.add_enable_disable("divide_in_chapters", ["chapter_size_spinbutton"], [])
        self.add_enable_disable("video_rate_automatic", [], ["video_spinbutton"])
        self.add_enable_disable("audio_rate_automatic", [], ["audio_spinbutton"])
        self.add_enable_disable("sound5_1", ["copy_sound"], [])

        self.add_enable_disable("copy_sound", [], ["audio_delay_spinbutton","audio_rate_automatic","audio_spinbutton","spinbutton_volume","scale_volume","reset_volume"])

        common_elements = ["gop12","video_rate_automatic","video_spinbutton","audio_rate_automatic","audio_spinbutton","format_pal","format_ntsc","spinbutton_volume","scale_volume","reset_volume",
                          "size_auto", "size_1920x1080", "size_1280x720", "size_720x576", "size_704x576", "size_480x576","size_352x576", "size_352x288",
                          "size_auto_ntsc", "size_1920x1080_ntsc", "size_1280x720_ntsc", "size_720x480_ntsc", "size_704x480_ntsc", "size_480x480_ntsc","size_352x480_ntsc", "size_352x240_ntsc",
                          "aspect_auto","aspect_classic","aspect_wide","mirror_horizontal","mirror_vertical","add_black_bars","scale_picture","cut_picture",
                          "rotation_0","rotation_90","rotation_180","rotation_270","two_pass_encoding","deinterlace_none","deinterlace_ffmpeg","deinterlace_yadif",
                          "audio_delay_spinbutton","sound5_1","copy_sound"]

        is_mpeg_ps_list = common_elements[:]
        is_mpeg_ps_list.append("no_reencode_audio_video")
        is_mpeg_ps_list.append("font_size_spinbutton")
        is_mpeg_ps_list.append("force_subtitles")
        is_mpeg_ps_list.append("add_subtitles")
        is_mpeg_ps_list.append("del_subtitles")
        no_reencode_audio_video_list = common_elements[:]
        no_reencode_audio_video_list.append("is_mpeg_ps")

        self.add_enable_disable("is_mpeg_ps", [], is_mpeg_ps_list)
        self.add_enable_disable("no_reencode_audio_video", [], no_reencode_audio_video_list)

        cv = devede.converter.converter()
        film_analizer = (cv.get_film_analizer())()
        if (film_analizer.get_film_data(self.file_name)):
            self.error = True
        else:
            self.audio_list = film_analizer.audio_list
            self.audio_streams = film_analizer.audio_streams
            self.video_streams = film_analizer.video_streams
            self.original_width = film_analizer.original_width
            self.original_height = film_analizer.original_height
            self.original_length = film_analizer.original_length
            self.original_size = film_analizer.original_size
            self.original_aspect_ratio = film_analizer.original_aspect_ratio
            self.original_videorate = film_analizer.original_videorate
            self.original_audiorate = film_analizer.original_audiorate
            self.original_audiorate_uncompressed = film_analizer.original_audiorate_uncompressed
            self.original_fps = film_analizer.original_fps
            self.error = False

        self.width_midle = -1
        self.height_midle = -1
        self.width_final = -1
        self.height_final = -1
        self.video_rate_final = self.video_rate
        self.audio_rate_final = self.audio_rate
        self.aspect_ratio_final = None

    def get_max_resolution(self,rx,ry,aspect):
        
        tmpx = ry*aspect
        tmpy = rx/aspect
        if (tmpx > rx):
            return tmpx,ry
        else:
            return rx,tmpy

    def set_final_size_aspect(self):
        
        if self.format_pal:
            final_size = self.final_size_pal
        else:
            final_size = self.final_size_ntsc[:-5] # remove the "_ntsc" from the string

        # for divx or matroska, if the size and the aspect ratio is automatic, just don't change them
        if ((self.disc_type == "divx") or (self.disc_type == "mkv")) and (final_size == "size_auto") and (self.aspect_ratio == "aspect_auto"):
            self.width_midle = self.original_width
            self.width_final = self.original_width
            self.height_midle = self.original_height
            self.height_final = self.original_height
            self.aspect_ratio_final = self.original_aspect_ratio
            return

        # The steps are:
        # - Decide the final aspect ratio
        # - Calculate the midle size: the original video will be scaled to this size
        # - Calculate the final size: the midle video will be cut to this size, or black bars will be added

        aspect_wide = False
        # first, decide the final aspect ratio
        if (self.disc_type == "vcd") or (self.disc_type == "svcd") or (self.disc_type == "cvd"):
            self.aspect_ratio_final = 4.0/3.0
        else:
            if (self.aspect_ratio == "aspect_auto"):
                if (self.disc_type != "dvd"):
                    self.aspect_ratio_final = self.original_aspect_ratio
                else:
                    if self.original_aspect_ratio >= 1.7:
                        self.aspect_ratio_final = 16.0/9.0
                        aspect_wide = True
                    else:
                        self.aspect_ratio_final = 4.0/3.0
            elif (self.aspect_ratio == "aspect_classic"):
                self.aspect_ratio_final = 4.0/3.0
            else:
                self.aspect_ratio_final = 16.0/9.0
                aspect_wide = True

        # now, the final resolution
        if self.disc_type == "vcd":
            self.width_final = 352
            if (self.format_pal):
                self.height_final = 288
            else:
                self.height_final = 240
        else:
            if final_size == "size_auto":
                if self.disc_type == "svcd":
                    self.width_final =480
                    if (self.format_pal):
                        self.height_final = 576
                    else:
                        self.height_final = 480
                elif self.disc_type == "cvd":
                    self.width_final =352
                    if (self.format_pal):
                        self.height_final = 288
                    else:
                        self.height_final = 240
                elif self.disc_type == "dvd":
                    if aspect_wide:
                        self.width_final = 720
                        if (self.format_pal):
                            self.height_final = 576
                        else:
                            self.height_final = 480
                    else:
                        tx, ty = self.get_max_resolution(self.original_width,self.original_height,self.original_aspect_ratio)
                        if (self.format_pal):
                            th = 576
                            th2 = 288
                        else:
                            th = 480
                            th2 = 240
                        if ( tx <= 352 ) and (ty <= th2):
                            self.width_final = 352
                            self.height_final = th2
                        elif (tx <= 352) and (ty <= th):
                            self.width_final = 352
                            self.height_final = th
                        elif (tx <= 704) and (ty <= th):
                            self.width_final = 704
                            self.height_final = th
                        else:
                            self.width_final = 720
                            self.height_final = th
                else:
                    self.width_final , self.height_final = self.get_max_resolution(self.original_width,self.original_height,self.original_aspect_ratio)
            else:
                values = final_size[5:].split("x")
                self.width_final = int(values[0])
                self.height_final = int(values[1])

        # finally, calculate the midle size
        
        if (self.rotation == "rotation_90") or (self.rotation == "rotation_270"):
            midle_aspect_ratio = 1.0 / self.original_aspect_ratio
        else:
            midle_aspect_ratio = self.original_aspect_ratio
        
        if self.scaling == "scale_picture":
            self.width_midle = self.width_final
            self.height_midle = self.height_final
        elif self.scaling == "add_black_bars":
            if midle_aspect_ratio > self.aspect_ratio_final: # add horizontal black bars, at top and bottom
                self.width_midle = self.width_final
                self.height_midle = self.height_final * self.aspect_ratio_final / midle_aspect_ratio
            else: # add vertical black bars, at left and right
                self.width_midle = self.height_final * midle_aspect_ratio
                self.height_midle = self.original_height
        else: # cut picture
            #if midle_aspect_ratio > self.aspect_ratio_final: # add horizontal black bars, at top and bottom
            self.width_midle = self.width_final
            self.height_midle = self.height_final # temporal option, until I do the calculations


    def set_type(self,obj = None,disc_type = None):

        if (disc_type != None):
            self.disc_type = disc_type


    def delete_file(self):

        print("Deleted file "+self.file_name)

    def properties(self):

        if (self.wfile_properties != None):
            self.wfile_properties.present()
            return

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(self.config.gettext_domain)

        self.builder.add_from_file(os.path.join(self.config.glade,"wfile_properties.ui"))
        self.builder.connect_signals(self)
        self.wfile_properties = self.builder.get_object("file_properties")
        self.wfile_properties.show_all()

        self.wshow_in_menu = self.builder.get_object("show_in_menu")

        self.wnotebook = self.builder.get_object("notebook")

        # elements in page GENERAL
        self.wframe_video_rate = self.builder.get_object("frame_video_rate")
        self.wframe_audio_rate = self.builder.get_object("frame_audio_rate")
        self.wframe_division_chapters = self.builder.get_object("frame_division_chapters")

        # elements in page SUBTITLES
        self.wsubtitles_list = self.builder.get_object("subtitles_list")
        self.wtreview_subtitles = self.builder.get_object("treeview_subtitles")
        self.wdel_subtitles = self.builder.get_object("del_subtitles")

        # elements in page VIDEO OPTIONS
        self.wsize_1920x1080 = self.builder.get_object("size_1920x1080")
        self.wsize_1280x720 = self.builder.get_object("size_1280x720")
        self.wsize_1920x1080_ntsc = self.builder.get_object("size_1920x1080_ntsc")
        self.wsize_1280x720_ntsc = self.builder.get_object("size_1280x720_ntsc")
        self.wframe_final_size = self.builder.get_object("frame_final_size")
        self.wframe_aspect_ratio = self.builder.get_object("frame_aspect_ratio")
        self.waspect_classic = self.builder.get_object("aspect_classic")
        self.wadd_black_bars_pic = self.builder.get_object("add_black_bars_pic")
        self.wscale_picture_pic = self.builder.get_object("scale_picture_pic")
        self.wcut_picture_pic = self.builder.get_object("cut_picture_pic")

        # elements in page AUDIO
        self.wsound5_1 = self.builder.get_object("sound5_1")
        self.wcopy_sound = self.builder.get_object("copy_sound")

        # Adjust the interface UI to the kind of disc

        if (self.disc_type == 'dvd'):
            self.wsize_1920x1080.hide()
            self.wsize_1280x720.hide()
            self.wsize_1920x1080_ntsc.hide()
            self.wsize_1280x720_ntsc.hide()
        elif (self.disc_type == 'vcd'):
            self.wshow_in_menu.hide()
            self.wframe_video_rate.hide()
            self.wframe_audio_rate.hide()
            self.wframe_division_chapters.hide()
            self.wframe_final_size.hide()
            self.wframe_aspect_ratio.hide()
            self.wsound5_1.hide()
            self.wcopy_sound.hide()
            self.wnotebook.remove_page(5)
        elif (self.disc_type == 'svcd'):
            self.wsize_1920x1080.hide()
            self.wsize_1280x720.hide()
            self.wsize_1920x1080_ntsc.hide()
            self.wsize_1280x720_ntsc.hide()
            self.wshow_in_menu.hide()
            self.wframe_division_chapters.hide()
            self.wframe_aspect_ratio.hide()
            self.wsound5_1.hide()
            self.wcopy_sound.hide()
            self.wnotebook.remove_page(5)
        elif (self.disc_type == 'cvd'):
            self.wsize_1920x1080.hide()
            self.wsize_1280x720.hide()
            self.wsize_1920x1080_ntsc.hide()
            self.wsize_1280x720_ntsc.hide()
            self.wshow_in_menu.hide()
            self.wframe_division_chapters.hide()
            self.wframe_aspect_ratio.hide()
            self.wsound5_1.hide()
            self.wcopy_sound.hide()
            self.wnotebook.remove_page(5)
        elif (self.disc_type == 'divx'):
            self.wshow_in_menu.hide()
            self.wframe_division_chapters.hide()
            self.wsound5_1.hide()
            self.wcopy_sound.hide()
            self.wnotebook.remove_page(5)
            self.wnotebook.remove_page(1)
        elif (self.disc_type == 'mkv'):
            self.wshow_in_menu.hide()
            self.wframe_division_chapters.hide()
            self.wnotebook.remove_page(5)

        self.update_ui(self.builder)
        self.on_aspect_classic_toggled(None)
        self.on_treeview_subtitles_cursor_changed(None)

    def on_aspect_classic_toggled(self,b):

        status = self.waspect_classic.get_active()
        if (status):
            self.wadd_black_bars_pic.set_from_file(os.path.join(self.config.pic_path,"to_classic_blackbars.png"))
            self.wcut_picture_pic.set_from_file(os.path.join(self.config.pic_path,"to_classic_cut.png"))
            self.wscale_picture_pic.set_from_file(os.path.join(self.config.pic_path,"to_classic_scale.png"))
        else:
            self.wadd_black_bars_pic.set_from_file(os.path.join(self.config.pic_path,"to_wide_blackbars.png"))
            self.wcut_picture_pic.set_from_file(os.path.join(self.config.pic_path,"to_wide_cut.png"))
            self.wscale_picture_pic.set_from_file(os.path.join(self.config.pic_path,"to_wide_scale.png"))

    def on_button_accept_clicked(self,b):

        self.store_ui(self.builder)
        self.emit('title_changed',self.title_name)
        self.on_button_cancel_clicked(None)

    def on_button_cancel_clicked(self,b):

        self.wfile_properties.destroy()
        self.wfile_properties = None
        self.builder = None

    def on_add_subtitles_clicked(self,b):

        subt = devede.ask_subtitles.ask_subtitles()
        if (subt.run()):
            self.wsubtitles_list.append([subt.filename, subt.encoding, subt.language, subt.put_upper])

    def get_selected_subtitle(self):

        selection = self.wtreview_subtitles.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter != None:
            return ( (model, treeiter) )
        else:
            return ( (None, None) )

    def on_del_subtitles_clicked(self,b):

        model, treeiter = self.get_selected_subtitle()
        if (model != None):
            model.remove(treeiter)

    def on_treeview_subtitles_cursor_changed(self,b):

        model, treeiter = self.get_selected_subtitle()
        if (model == None):
            self.wdel_subtitles.set_sensitive(False)
        else:
            self.wdel_subtitles.set_sensitive(True)
    
    
    def do_conversion(self, output_path, duration = 0):
        
        self.set_final_size_aspect()
        cv = devede.converter.converter()
        disc_converter = cv.get_disc_converter()
        converter = disc_converter()
        converter.convert_file(self,output_path,duration)
        return converter
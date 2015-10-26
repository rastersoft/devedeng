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

from gi.repository import Gtk, Gdk
import os
import time
import shutil
import urllib.parse
import pickle
import math

import devedeng.file_movie
import devedeng.ask
import devedeng.add_files
import devedeng.message
import devedeng.dvd_menu
import devedeng.create_disk_window
import devedeng.runner
import devedeng.settings
import devedeng.dvdauthor_converter
import devedeng.mkisofs
import devedeng.end_job
import devedeng.vcdimager_converter
import devedeng.shutdown
import devedeng.about
import devedeng.opensave
import devedeng.help

class devede_project:

    def __init__(self):

        self.config  = devedeng.configuration_data.configuration.get_config()

        self.disc_type = self.config.disc_type
        self.menu = devedeng.dvd_menu.dvd_menu()

        self.current_title = None
        self.project_file = None

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(self.config.glade,"wmain.ui"))
        builder.connect_signals(self)

        # Interface widgets
        self.wmain_window = builder.get_object("wmain_window")
        self.wdisc_size = builder.get_object("disc_size")
        self.wliststore_files = builder.get_object("liststore_files")
        self.wfiles = builder.get_object("files")
        self.wdisc_fill_level = builder.get_object("disc_fill_level")
        self.wuse_pal = builder.get_object("use_pal")
        self.wuse_ntsc = builder.get_object("use_ntsc")
        self.wframe_titles = builder.get_object("frame_titles")

        self.wframe_menu = builder.get_object("frame_menu")
        self.wcreate_menu = builder.get_object("create_menu")
        self.wmenu_options = builder.get_object("menu_options")


        self.wadd_file = builder.get_object("add_file")
        self.wdelete_file = builder.get_object("delete_file")
        self.wup_file = builder.get_object("up_file")
        self.wdown_file = builder.get_object("down_file")
        self.wproperties_file = builder.get_object("properties_file")
        self.wpreview_file = builder.get_object("preview_file")

        self.wcreate_disc = builder.get_object("create_disc")

        selection = self.wfiles.get_selection()
        selection.set_mode(Gtk.SelectionMode.BROWSE)

        if (self.config.PAL):
            self.wuse_pal.set_active(True)
            self.pal = True
        else:
            self.wuse_ntsc.set_active(True)
            self.pal = False

        self.wcreate_menu.set_active(True)

        self.config.connect('disc_type',self.set_type)
        if (self.disc_type != None):
            self.set_type(None, self.disc_type)

        self.wmain_window.drag_dest_set(Gtk.DestDefaults.ALL,[],Gdk.DragAction.COPY)
        targets = Gtk.TargetList.new([])
        targets.add(Gdk.Atom.intern("text/uri-list", False),0,0)
        self.wmain_window.drag_dest_set_target_list(targets)


    def set_type(self,obj=None,disc_type=None):
        """ this method sets the disk type to the specified one and adapts the interface
            in the main window to it. Also leaves everything ready to start creating a
            new disc """

        if (disc_type != None):
            self.disc_type = disc_type
        self.wmain_window.show_all()
        self.set_interface_status(None)

        # Set the default disc size
        if (self.disc_type == "dvd") or (self.disc_type == "mkv"):
            self.wdisc_size.set_active(1) # 4.7 GB DVD
        else:
            self.wdisc_size.set_active(3) # 700 MB CD

        if (self.disc_type == "dvd"):
            self.wframe_menu.show_all()
            self.wcreate_menu.set_active(True)
        else:
            self.wframe_menu.hide()
            self.wcreate_menu.set_active(False)


    def get_current_file(self):

        """ returns the currently selected file """

        selection = self.wfiles.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter != None:
            element = model[treeiter][0]
            position = 0
            for row in self.wfiles.get_model():
                item = row.model[row.iter][0]
                if element == item:
                    break
                position += 1
            return ( (element, position, model, treeiter) )
        else:
            return ( (None, -1, None, None) )


    def get_all_files(self):

        retval = []

        for row in self.wfiles.get_model():
            retval.append(row.model[row.iter][0])
        return retval


    def set_interface_status(self,b):

        self.wadd_file.set_sensitive(True)
        self.wdelete_file.set_sensitive(True)
        self.wup_file.set_sensitive(True)
        self.wdown_file.set_sensitive(True)
        self.wproperties_file.set_sensitive(True)
        self.wpreview_file.set_sensitive(True)

        status = self.wcreate_menu.get_active()
        self.wmenu_options.set_sensitive(status)

        self.pal = self.wuse_pal.get_active()

        (element, position, model, treeiter) = self.get_current_file()
        if (element == None):
            self.wdelete_file.set_sensitive(False)
            self.wup_file.set_sensitive(False)
            self.wdown_file.set_sensitive(False)
            self.wproperties_file.set_sensitive(False)
            self.wpreview_file.set_sensitive(False)
        else:
            nfiles = len(self.wfiles.get_model())
            if (nfiles < 1):
                self.wdelete_file.set_sensitive(False)
            if (position == 0):
                self.wup_file.set_sensitive(False)
            if (position == (nfiles-1)):
                self.wdown_file.set_sensitive(False)


    def on_cellrenderertext3_edited(self, widget, path, text):
        self.wliststore_files[path][0].set_title(text)


    def on_use_pal_toggled(self,b):

        self.config.PAL = self.wuse_pal.get_active()
        self.set_interface_status(None)


    def on_wmain_window_delete_event(self,b,e=None):

        ask = devedeng.ask.ask_window()
        if (ask.run(_("Abort the current DVD and exit?"),_("Exit DeVeDe"))):
            Gtk.main_quit()
        return True

    def title_changed(self,obj,new_title):

        for item in self.wliststore_files:
            element = item.model[item.iter][0]
            if element == obj:
                item.model.set_value(item.iter,1,new_title)
        self.refresh_disc_usage()


    def on_help_clicked(self,b):
        
        help_file = devedeng.help.help("main.html")

    def on_help_index_activate(self,b):
        
        help_file = devedeng.help.help("index.html")


    def on_add_file_clicked(self,b):

        ask_files = devedeng.add_files.add_files()
        if (ask_files.run()):
            self.add_several_files(ask_files.files)


    def duration_to_string(self,duration):

        seconds = math.floor(duration%60)
        minutes = math.floor((duration/60)%60)
        hours = math.floor(duration/3600)

        output = str(seconds)+"s"
        if ((hours != 0) or (minutes != 0)):
            output = str(minutes)+"m "+output
        if (hours != 0):
            output = str(hours)+"h "+output
        return output


    def add_several_files(self,file_list):
        error_list = []
        for efile in file_list:
            if efile.startswith("file://"):
                efile = urllib.parse.unquote(efile[7:])
            new_file = devedeng.file_movie.file_movie(efile)
            if (new_file.error):
                error_list.append(os.path.basename(efile))
            else:
                new_file.connect('title_changed',self.title_changed)
                self.wliststore_files.append([new_file, new_file.title_name,True,self.duration_to_string(new_file.get_duration())])
        if (len(error_list)!=0):
            devedeng.message.message_window(_("The following files could not be added:"),_("Error while adding files"),error_list)
        self.set_interface_status(None)
        self.refresh_disc_usage()


    def on_delete_file_clicked(self,b):

        (element, position, model, treeiter) = self.get_current_file()
        if (element == None):
            return

        ask_w = devedeng.ask.ask_window()
        if (ask_w.run(_("The file <b>%(X)s</b> <i>(%(Y)s)</i> will be removed.") % {"X":element.title_name, "Y":element.file_name},_("Delete file"))):
            element.delete_file()
            model.remove(treeiter)
            self.set_interface_status(None)
            self.refresh_disc_usage()


    def on_up_file_clicked(self,b):

        (element, position, model, treeiter) = self.get_current_file()
        if (element == None) or (position == 0):
            return

        last_element = self.wfiles.get_model()[position-1]
        self.wfiles.get_model().swap(last_element.iter,treeiter)
        self.set_interface_status(None)


    def on_down_file_clicked(self,b):

        (element, position, model, treeiter) = self.get_current_file()
        if (element == None) or (position == (len(self.wfiles.get_model())-1)):
            return

        last_element = self.wfiles.get_model()[position+1]
        self.wfiles.get_model().swap(last_element.iter,treeiter)
        self.set_interface_status(None)


    def on_properties_file_clicked(self,b):
        (element, position, model, treeiter) = self.get_current_file()
        if (element == None):
            return
        element.properties()


    def on_create_menu_toggled(self,b):
        self.set_interface_status(None)
        self.refresh_disc_usage()


    def on_adjust_disc_usage_clicked(self,b):

        total_resolution = 0
        fixed_size = 0
        to_adjust = []
        for f in self.get_all_files():
            estimated_size, videorate_fixed_size, audio_rate, sub_rate, width, height, time_length = f.get_size_data()
            if videorate_fixed_size:
                fixed_size += estimated_size
            else:
                fixed_size += ((audio_rate + sub_rate) * time_length)
                # 76800 = 320x240, which is the smallest resolution
                surface = ((float(width) * float(height)) / 76800.0) * float(time_length)
                to_adjust.append( (f, surface, time_length, audio_rate, height) )
                total_resolution += surface

        if (self.disc_type == "dvd") and (self.wcreate_menu.get_active()):
            fixed_size += self.menu.get_estimated_size() * 8.0

        if (self.disc_type == "dvd"):
            max_bps_base = {0: 9000}
            min_bps = 300
            max_total = 10000
        elif (self.disc_type == "svcd") or (self.disc_type == "cvd"):
            max_bps_base = {0: 2700}
            min_bps = 200
            max_total = 2700
        elif (self.disc_type == "divx"):
            max_bps_base = {0: 4854, 720: 9708, 1080: 20000}
            min_bps = 300
            max_total = -1
        elif (self.disc_type == "mkv"):
            max_bps_base = {0: 192, 240: 2000, 480: 14000,  720: 50000, 1080: 240000}
            min_bps = 192
            max_total = -1
        else:
            max_bps_base = {0: 9000}
            min_bps = 300
            max_total = -1

        if (total_resolution != 0):
            remaining_disc_size = ((8000.0 * self.get_dvd_size()[0]) - fixed_size) # in kbits
            for l in to_adjust:
                f = l[0]
                surface = l[1]
                length = l[2]
                audio_rate = l[3]
                height = l[4]

                max_bps = max_bps_base[0]
                resy = 0
                for bitrates in max_bps_base:
                    if (height >= bitrates) and (resy < bitrates):
                        resy = bitrates
                        max_bps = max_bps_base[bitrates]

                video_rate = (remaining_disc_size * surface) / ( length * total_resolution)
                if max_total != -1:
                    max2 = max_total - audio_rate
                    if (max2 > max_bps):
                        max2 = max_bps
                else:
                    max2 = max_bps
                if (video_rate > max2):
                    video_rate = max2
                if (video_rate < min_bps):
                    video_rate = min_bps
                f.set_auto_video_audio_rate(video_rate, audio_rate)

        self.refresh_disc_usage()


    def refresh_disc_usage(self):

        used = 0.0

        for f in self.get_all_files():
            estimated_size = f.get_estimated_size()
            used += float(estimated_size)

        if self.wcreate_menu.get_active():
            used += float(self.menu.get_estimated_size())

        used /= 1000.0

        disc_size,minvrate,maxvrate = self.get_dvd_size()

        if used > disc_size:
            self.wdisc_fill_level.set_fraction(1.0)
            addv=1
        else:
            self.wdisc_fill_level.set_fraction(used / disc_size)
            addv=0

        self.wdisc_fill_level.set_text(str(addv+int((used / disc_size)*100))+"%")
        self.wdisc_fill_level.set_show_text(True)


    def on_menu_options_clicked(self,b):

        self.menu.show_configuration(self.get_all_files())


    def get_dvd_size(self):

        """ Returns the size for the currently selected disk type, and the minimum and maximum
            videorate for the current video disk """

        active = self.wdisc_size.get_active()

        # here we choose the size in Mbytes for the media
        if 5==active:
            size=170.0
        elif 4==active:
            size=700.0
        elif 3==active:
            size=750.0
        elif 2==active:
            size=1100.0
        elif 1==active:
            size=4200.0
        else:
            size=8000.0

        if self.disc_type=="vcd":
            minvrate=1152
            maxvrate=1152
        elif (self.disc_type == "svcd") or (self.disc_type == "cvd"):
            minvrate=400
            maxvrate=2300
        elif (self.disc_type == "dvd"):
            minvrate=400
            maxvrate=8500
        elif (self.disc_type == "divx") or (self.disc_type == "mkv"):
            minvrate=300
            maxvrate=6000
        else:
            minvrate = 0
            maxvrate = 8000

        size *= 0.90  # a safe margin of 10% to ensure that it never will be bigger
                    # (it's important to have in mind the space needed by disk structures like
                    # directories, file entries, and so on)

        return size,minvrate,maxvrate


    def on_disc_size_changed(self,c):

        self.refresh_disc_usage()


    def on_create_disc_clicked(self,b):

        if self.disc_type == "dvd":
            max_files = 62
        else:
            max_files = -1

        file_movies = self.get_all_files()
        t = len(file_movies)
        if (max_files != -1) and (t > max_files):
            devedeng.message.message_window(_("The limit for this format is %(l)d files, but your project has %(h)d.") % {"l": max_files, "h" : t}, _("Too many files in the project"))
            return

        data = devedeng.create_disk_window.create_disk_window()
        if (not data.run()):
            return

        if os.path.exists(data.path):
            ask_w = devedeng.ask.ask_window()
            retval = ask_w.run(_("The selected folder already exists. To create the project, Devede must delete it.\nIf you continue, the folder\n\n <b>%s</b>\n\n and all its contents <b>will be deleted</b>. Continue?") % data.path,_("Delete folder"))
            if retval:
                # delete only the bare minimun needed
                shutil.rmtree(os.path.join(data.path,"dvd_tree"),True)
                shutil.rmtree(os.path.join(data.path,"menu"),True)
                shutil.rmtree(os.path.join(data.path,"movies"),True)
                shutil.rmtree(os.path.join(data.path,"xml_data"),True)
                if self.config.disc_type == "dvd":
                    try:
                        os.unlink(os.path.join(data.path,data.name+".iso"))
                    except:
                        pass
                if (self.config.disc_type == "vcd") or (self.config.disc_type == "svcd") or (self.config.disc_type == "cvd"):
                    try:
                        os.unlink(os.path.join(data.path,data.name+".bin"))
                    except:
                        pass
                    try:
                        os.unlink(os.path.join(data.path,data.name+".cue"))
                    except:
                        pass
            else:
                return

        self.shutdown = data.shutdown

        run_window = devedeng.runner.runner()

        final_dependencies = []

        if (self.disc_type == "dvd") and (self.wcreate_menu.get_active()):
            processes,menu_entries = self.menu.create_dvd_menus(file_movies, data.path)
            for p in processes:
                run_window.add_process(p)
                final_dependencies.append(p)
        else:
            menu_entries = None

        movie_folder = os.path.join(data.path,"movies")
        try:
            os.makedirs(movie_folder)
        except:
            pass
        counter = 0
        for movie in file_movies:
            p = movie.do_conversion(os.path.join(movie_folder,"movie_"+str(counter)+".mpg"))
            run_window.add_process(p)
            final_dependencies.append(p)
            counter += 1

        if (self.disc_type == "dvd"):
            if (self.menu.at_startup == "menu_show_at_startup"):
                start_with_menu = True
            else:
                start_with_menu = False
            if (self.menu.play_all == "menu_play_all"):
                play_all_opt = True
            else:
                play_all_opt = False
            dvdauthor = devedeng.dvdauthor_converter.dvdauthor_converter()
            dvdauthor.create_dvd_project(data.path, data.name, file_movies, menu_entries, start_with_menu, play_all_opt)
            # dvdauthor must wait until all the files have been converted
            for element in final_dependencies:
                dvdauthor.add_dependency(element)
            run_window.add_process(dvdauthor)

            cv = devedeng.converter.converter.get_converter()
            isocreator = cv.get_mkiso()()
            isocreator.create_iso(data.path, data.name)
            isocreator.add_dependency(dvdauthor)
            run_window.add_process(isocreator)
            self.disc_image_name = os.path.join(data.path,data.name+".iso")
        elif (self.disc_type == "vcd") or (self.disc_type == "svcd") or (self.disc_type == "cvd"):
            vcdcreator = devedeng.vcdimager_converter.vcdimager_converter()
            vcdcreator.create_cd_project(data.path, data.name, file_movies)
            for element in final_dependencies:
                vcdcreator.add_dependency(element)
            run_window.add_process(vcdcreator)
            self.disc_image_name = os.path.join(data.path,data.name+".cue")
        else:
            self.disc_image_name = None

        run_window.connect("done",self.disc_done)
        self.wmain_window.hide()
        self.time_start = time.time()
        run_window.run()


    def disc_done(self,object,value):

        if self.shutdown:
            Gtk.main_quit()
            devedeng.shutdown.shutdown()

        if value == 0:
            ended = devedeng.end_job.end_window()
            if self.disc_image_name == None:
                do_burn = False
            else:
                do_burn = True
            if (ended.run(time.time() - self.time_start, do_burn)):
                cv = devedeng.converter.converter.get_converter()
                burner = cv.get_burner()()
                burner.burn(self.disc_image_name)
                run_window = devedeng.runner.runner(False)
                run_window.add_process(burner)
                run_window.connect("done", self.disc_done2)
                run_window.run()
                return

        self.wmain_window.show()


    def disc_done2(self,object, value):

        self.wmain_window.show()


    def on_preview_file_clicked(self,b):

        (element, position, model, treeiter) = self.get_current_file()
        if (element == None):
            return
        element.do_preview()


    def on_settings_activate(self,b):

        w = devedeng.settings.settings_window()


    def on_about_activate(self,b):

        w = devedeng.about.about_window()


    def on_new_activate(self,b):

        w = devedeng.ask.ask_window()
        if w.run(_("Close current project and start a fresh one?"), _("New project")):
            self.wliststore_files.clear()
            self.project_file = None
            self.wmain_window.hide()
            devedeng.choose_disc_type.choose_disc_type()


    def on_wmain_window_drag_motion(self,wid, context, x, y, time):
        Gdk.drag_status(context, Gdk.DragAction.COPY, time)
        return True


    def on_wmain_window_drag_drop(self, wid, context, x, y, time):
        # Used with windows drag and drop
        return True


    def on_wmain_window_drag_data_received(self, widget, drag_context, x,y, data, info, time):
        uris = data.get_uris()
        self.add_several_files(uris)
        Gtk.drag_finish (drag_context, True, Gdk.DragAction.COPY, time);


    def on_save_activate(self,b):
        if self.project_file != None:
            self.save_current_project()
        else:
            self.on_save_as_activate(None)


    def on_save_as_activate(self,b):

        while True:
            w = devedeng.opensave.opensave_window(True)
            retval = w.run(self.project_file)
            if retval == None:
                return
            if not retval.endswith(".devedeng"):
                retval += ".devedeng"
            if os.path.isfile(retval):
                w = devedeng.ask.ask_window()
                if not w.run(_("The file already exists. Overwrite it?"), _("The file already exists")):
                    continue
            self.project_file = retval
            self.save_current_project()
            return


    def on_load_activate(self,b):
        w = devedeng.opensave.opensave_window(False)
        retval = w.run()
        if retval != None:
            self.load_project(retval)


    def save_current_project(self):

        project = {}

        project["PAL"] = self.wuse_pal.get_active()
        project["create_menu"] = self.wcreate_menu.get_active()
        project["disc_type"] = self.config.disc_type
        project["disc_size"] = self.wdisc_size.get_active()
        project["files"] = []
        f = self.get_all_files()
        for i in f:
            project["files"].append(i.store_file())
        if self.disc_type == "dvd":
            project["menu"] = self.menu.store_menu()

        with open(self.project_file, 'wb') as f:
            pickle.dump(project, f, 3)


    def load_project(self,project_file):

        self.wliststore_files.clear()
        self.project_file = project_file
        with open(project_file, 'rb') as f:
            project = pickle.load(f)
        if "disc_type" in project:
            self.config.set_disc_type(project["disc_type"])
        if "PAL" in project:
            self.wuse_pal.set_active(project["PAL"])
        if "create_menu" in project:
            self.wcreate_menu.set_active(project["create_menu"])
        if "disc_size" in project:
            self.wdisc_size.set_active(project["disc_size"])
        if "menu" in project:
            self.menu.restore_menu(project["menu"])
        if "files" in project:
            error_list = []
            for efile in project["files"]:
                new_file = devedeng.file_movie.file_movie(efile["file_name"])
                if (new_file.error):
                    error_list.append(os.path.basename(efile["file_name"]))
                else:
                    new_file.restore_file(efile)
                    new_file.connect('title_changed',self.title_changed)
                    self.wliststore_files.append([new_file, new_file.title_name,True,self.duration_to_string(new_file.get_duration())])
            if (len(error_list)!=0):
                devedeng.message.message_window(_("The following files in the project could not be added again:"),_("Error while adding files"),error_list)
        self.set_interface_status(None)
        self.refresh_disc_usage()


    def on_multiproperties_activate(self,b):

        e = devedeng.file_movie.file_movie(None,self.get_all_files())
        e.properties()

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

from gi.repository import Gtk
import os
import time

import devede.file_movie
import devede.ask
import devede.add_files
import devede.message
import devede.dvd_menu
import devede.create_disk_window
import devede.runner
import devede.settings
import devede.dvdauthor_converter
import devede.mkisofs
import devede.end_job
import devede.vcdimager_converter

class devede_project:

    def __init__(self):

        self.config  = devede.configuration_data.configuration.get_config()

        self.disc_type = self.config.disc_type
        self.menu = devede.dvd_menu.dvd_menu()

        self.current_title = None

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
        selection.mode = Gtk.SelectionMode.SINGLE

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
        else:
            self.wframe_menu.hide()


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


    def on_use_pal_toggled(self,b):

        self.config.PAL = self.wuse_pal.get_active()
        self.set_interface_status(None)



    def on_wmain_window_delete_event(self,b,e=None):

        ask = devede.ask.ask_window()
        if (ask.run(_("Abort the current DVD and exit?"),_("Exit DeVeDe"))):
            Gtk.main_quit()
        return True

    def title_changed(self,obj,new_title):

        for item in self.wliststore_files:
            element = item.model[item.iter][0]
            if element == obj:
                item.model.set_value(item.iter,1,new_title)
        self.refresh_disc_usage()


    def on_add_file_clicked(self,b):

        error_list = []
        ask_files = devede.add_files.add_files()
        if (ask_files.run()):
            for efile in ask_files.files:
                new_file = devede.file_movie.file_movie(efile)
                if (new_file.error):
                    error_list.append(os.path.basename(efile))
                else:
                    new_file.connect('title_changed',self.title_changed)
                    self.wliststore_files.append([new_file, new_file.title_name])
        if (len(error_list)!=0):
            devede.message.message_window(_("The following files could not be added:"),_("Error while adding files"),error_list)
        self.set_interface_status(None)
        self.refresh_disc_usage()


    def on_delete_file_clicked(self,b):

        (element, position, model, treeiter) = self.get_current_file()
        if (element == None):
            return

        ask_w = devede.ask.ask_window()
        if (ask_w.run(_("The file <b>%(X)s</b> <i>(%(Y)s)</i> will be removed.") % {"X":element.title_name, "Y":element.file_name},_("Delete file"))):
            element.delete_file()
            model.remove(treeiter)
            self.set_interface_status(None)

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
                fixed_size += ((audio_rate + sub_rate) * time_length) / 8
                # 76800 = 320x240, which is the smallest resolution
                surface = ((width * height) / 76800.0) * time_length
                to_adjust.append( (f, surface, time_length) )
                total_resolution += surface

        if (self.disc_type == "dvd") and (self.wcreate_menu.get_active()):
            fixed_size += self.menu.get_estimated_size()

        if (total_resolution != 0):
            remaining_disc_size = ((1000 * self.get_dvd_size()[0]) - fixed_size) * 8 # in kbits
            for l in to_adjust:
                f = l[0]
                surface = l[1]
                length = l[2]
                f.set_auto_video_rate((remaining_disc_size * surface) / (total_resolution * length))

        self.refresh_disc_usage()


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

        size*=0.90  # a safe margin of 10% to ensure that it never will be bigger
                    # (it's important to have in mind the space needed by disk structures like
                    # directories, file entries, and so on)

        return size,minvrate,maxvrate


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


    def on_disc_size_changed(self,c):

        self.refresh_disc_usage()


    def on_create_disc_clicked(self,b):

        data = devede.create_disk_window.create_disk_window()
        if (not data.run()):
            return

        run_window = devede.runner.runner()
        file_movies = self.get_all_files()

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
            dvdauthor = devede.dvdauthor_converter.dvdauthor_converter()
            dvdauthor.create_dvd_project(data.path, data.name, file_movies, menu_entries, start_with_menu)
            # dvdauthor must wait until all the files have been converted
            for element in final_dependencies:
                dvdauthor.add_dependency(element)
            run_window.add_process(dvdauthor)
            isocreator = devede.mkisofs.mkisofs()
            isocreator.create_iso(data.path, data.name)
            isocreator.add_dependency(dvdauthor)
            run_window.add_process(isocreator)
            self.disc_image_name = os.path.join(data.path,data.name+".iso")
        elif (self.disc_type == "vcd") or (self.disc_type == "svcd") or (self.disc_type == "cvd"):
            vcdcreator = devede.vcdimager_converter.vcdimager_converter()
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

        if value == 0:
            ended = devede.end_job.end_window()
            if self.disc_image_name == None:
                do_burn = False
            else:
                do_burn = True
            if (ended.run(time.time() - self.time_start, do_burn)):
                cv = devede.converter.converter.get_converter()
                burner = cv.get_burner()()
                burner.burn(self.disc_image_name)
                run_window = devede.runner.runner(False)
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

        w = devede.settings.settings_window()
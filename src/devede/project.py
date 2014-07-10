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

import devede.title


class devede_project:

    def __init__(self,paths):

        self.paths = paths
        self.destroy_all()
        
        
    def destroy_all(self):
        
        self.wask_window = None
        self.wmain_window = None
        self.wframe_titles = None
        self.wdisc_size = None
        self.wliststore_files = None
        self.wliststore_titles = None
        self.wfiles = None
        self.wtitles = None
        self.wdisc_fill_level = None
        self.wuse_pal = None
        self.wuse_ntsc = None
        self.wcreate_menu = None
        self.project_type = None
        self.wdelete_title = None
        self.wup_title = None
        self.wdown_title = None
        self.wproperties_title = None
        self.wadd_chapter = None
        self.wdelete_chapter = None
        self.wup_chapter = None
        self.wdown_chapter = None
        self.wproperties_chapter = None
        self.wcreate_disc = None
        
        devede.title.counter = 0


    def ask_type(self):
        """ This method resets the project and asks the user what kind of project want to do """

        if (self.wask_window != None):
            self.wask_window.present()
            return

        builder = Gtk.Builder()
        builder.set_translation_domain("devede_ng")

        builder.add_from_file(os.path.join(self.paths.glade,"wselect_disk.ui"))
        builder.connect_signals(self)
        self.wask_window = builder.get_object("wselect_disk")
        self.wask_window.show_all()

    def on_wselect_disk_delete_event(self,w,e):
        Gtk.main_quit()
        return False

    def on_button_dvd_clicked(self,b):

        self.set_type("dvd")

    def on_button_vcd_clicked(self,b):

        self.set_type("vcd")

    def on_button_svcd_clicked(self,b):

        self.set_type("svcd")

    def on_button_cvd_clicked(self,b):

        self.set_type("cvd")

    def on_button_divx_clicked(self,b):

        self.set_type("divx")


    def set_type(self,disc_type):
        """ this method sets the disk type to the specified one and adapts the interface
            in the main window to it. Also leaves everything ready to start creating a
            new disc """

        if (self.wask_window != None):
            self.wask_window.destroy()
        self.destroy_all()
        
        self.project_type = disc_type
        self.show_main_window()
        
        # Set the default disc size
        if (self.project_type == "dvd"):
            self.wdisc_size.set_active(1) # 4.7 GB DVD
            self.wframe_titles.show()
        else:
            self.wdisc_size.set_active(3) # 700 MB CD
            self.wframe_titles.hide()
            

        # create a new title
        self.on_add_title_clicked(None)


    def on_add_title_clicked(self,b):
        """ Creates a new title and adds it to the current project """
        
        self.get_current_title()
        
        new_title = devede.title.title()
        self.wliststore_titles.append([new_title.title_name, new_title])
        self.set_interface_status(None)


    def on_delete_title_clicked(self,b):
        
        (element, position, model, treeiter) = self.get_current_title()
        if (element == None):
            return
        
        element.delete_title()
        model.remove(treeiter)
        self.set_interface_status(None)

    def on_up_title_clicked(self,b):
        
        (element, position, model, treeiter) = self.get_current_title()
        if (element == None) or (position == 0):
            return
        
        last_element = self.wliststore_titles[position-1]
        self.wliststore_titles.swap(last_element.iter,treeiter)
        self.set_interface_status(None)
        
    def on_down_title_clicked(self,b):
        
        (element, position, model, treeiter) = self.get_current_title()
        if (element == None) or (position == (len(self.wliststore_titles)-1)):
            return
        
        last_element = self.wliststore_titles[position+1]
        self.wliststore_titles.swap(last_element.iter,treeiter)
        self.set_interface_status(None)

    def get_current_title(self):
        """ returns the currently selected title """

        selection = self.wtitles.get_selection()
        model, treeiter = selection.get_selected()
        
        if treeiter != None:
            element = model[treeiter][1]
            position = 0
            for row in self.wliststore_titles:
                item = row.model[row.iter][1]
                if element == item:
                    break
                position += 1
            return ( (element, position, model, treeiter) )
        else:
            return ( (None, -1, None, None) )
        


    def set_interface_status(self,b):
        
        self.wadd_title.set_sensitive(True)
        self.wdelete_title.set_sensitive(True)
        self.wup_title.set_sensitive(True)
        self.wdown_title.set_sensitive(True)
        self.wproperties_title.set_sensitive(True)
        
        self.wadd_chapter.set_sensitive(True)
        self.wdelete_chapter.set_sensitive(True)
        self.wup_chapter.set_sensitive(True)
        self.wdown_chapter.set_sensitive(True)
        self.wproperties_chapter.set_sensitive(True)
        
        self.wcreate_disc.set_sensitive(True)

        (element, position, model, treeiter) = self.get_current_title()
        
        if (element == None):
            self.wdelete_title.set_sensitive(False)
            self.wup_title.set_sensitive(False)
            self.wdown_title.set_sensitive(False)
            self.wproperties_title.set_sensitive(False)
            self.wadd_chapter.set_sensitive(False)
            self.wdelete_chapter.set_sensitive(False)
            self.wup_chapter.set_sensitive(False)
            self.wdown_chapter.set_sensitive(False)
            self.wproperties_chapter.set_sensitive(False)
        else:
            ntitles = len(self.wliststore_titles)
            if (ntitles < 2):
                self.wdelete_title.set_sensitive(False)
            if (position == 0):
                self.wup_title.set_sensitive(False)
            if (position == (ntitles-1)):
                self.wdown_title.set_sensitive(False)

        empty_disc = True
        for row in self.wliststore_titles:
            item = row.model[row.iter][1]
            if item.get_number_of_chapters() > 0:
                empty_disc = False
                break

        if (empty_disc):
            self.wcreate_disc.set_sensitive(False)



    def show_main_window(self):

        if (self.wmain_window != None):
            self.wmain_window.present()
            return

        builder = Gtk.Builder()
        builder.set_translation_domain("devede_ng")

        builder.add_from_file(os.path.join(self.paths.glade,"wmain.ui"))
        builder.connect_signals(self)

        # Interface widgets
        self.wmain_window = builder.get_object("wmain_window")
        self.wdisc_size = builder.get_object("disc_size")
        self.wliststore_files = builder.get_object("liststore_files")
        self.wliststore_titles = builder.get_object("liststore_titles")
        self.wfiles = builder.get_object("files")
        self.wtitles = builder.get_object("titles")
        self.wdisc_fill_level = builder.get_object("disc_fill_level")
        self.wuse_pal = builder.get_object("use_pal")
        self.wuse_ntsc = builder.get_object("use_ntsc")
        self.wcreate_menu = builder.get_object("create_menu")
        self.wframe_titles = builder.get_object("frame_titles")
        
        self.wadd_title = builder.get_object("delete_title")
        self.wdelete_title = builder.get_object("delete_title")
        self.wup_title = builder.get_object("up_title")
        self.wdown_title = builder.get_object("down_title")
        self.wproperties_title = builder.get_object("properties_title")
        self.wadd_chapter = builder.get_object("add_chapter")
        self.wdelete_chapter = builder.get_object("delete_chapter")
        self.wup_chapter = builder.get_object("up_chapter")
        self.wdown_chapter = builder.get_object("down_chapter")
        self.wproperties_chapter = builder.get_object("properties_chapter")
        
        self.wcreate_disc = builder.get_object("create_disc")
        
        selection = self.wfiles.get_selection()
        selection.mode = Gtk.SelectionMode.SINGLE
        selection = self.wtitles.get_selection()
        selection.mode = Gtk.SelectionMode.SINGLE

        self.wmain_window.show_all()
        

    def on_adjust_disc_usage_clicked(self,b):

        pass



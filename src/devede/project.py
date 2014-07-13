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

import devede.file_movie
import devede.ask
import devede.add_files

class devede_project:

    def __init__(self,config):

        self.config = config
        self.destroy_all()


    def destroy_all(self):

        self.wask_window = None
        self.wmain_window = None
        self.wdisc_size = None
        self.wliststore_files = None
        self.wfiles = None
        self.wdisc_fill_level = None
        self.wuse_pal = None
        self.wuse_ntsc = None
        self.wcreate_menu = None
        self.disc_type = None
        self.wadd_file = None
        self.wdelete_file = None
        self.wup_file = None
        self.wdown_file = None
        self.wproperties_file = None
        self.wcreate_disc = None


    def ask_type(self):
        """ This method resets the project and asks the user what kind of project want to do """

        if (self.wask_window != None):
            self.wask_window.present()
            return

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(self.config.glade,"wselect_disk.ui"))
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

        self.disc_type = disc_type
        self.show_main_window()

        # Set the default disc size
        if (self.disc_type == "dvd"):
            self.wdisc_size.set_active(1) # 4.7 GB DVD
        else:
            self.wdisc_size.set_active(3) # 700 MB CD


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



    def set_interface_status(self,b):

        self.wadd_file.set_sensitive(True)
        self.wdelete_file.set_sensitive(True)
        self.wup_file.set_sensitive(True)
        self.wdown_file.set_sensitive(True)
        self.wproperties_file.set_sensitive(True)
        self.wpreview_file.set_sensitive(True)

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


    def show_main_window(self):

        if (self.wmain_window != None):
            self.wmain_window.present()
            return

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
        self.wcreate_menu = builder.get_object("create_menu")
        self.wframe_titles = builder.get_object("frame_titles")

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
        else:
            self.wuse_ntsc.set_active(True)
        self.wmain_window.show_all()
        self.set_interface_status(None)

    def on_use_pal_toggled(self,b):
        
        self.config.PAL = self.wuse_pal.get_active()

    def on_wmain_window_delete_event(self,b,e=None):

        ask = devede.ask.ask_window(self.config)
        if (ask.run(_("Abort the current DVD and exit?"),_("Exit DeVeDe"))):
            Gtk.main_quit()
        return True

    def on_add_file_clicked(self,b):

        ask_files = devede.add_files.add_files(self.config)
        ask_files.set_type(self.disc_type)
        if (ask_files.run()):
            for efile in ask_files.files:
                new_file = devede.file_movie.file_movie(self.config,efile)
                new_file.set_type(self.disc_type)
                self.wliststore_files.append([new_file, new_file.title_name])
        self.set_interface_status(None)


    def on_delete_file_clicked(self,b):

        (element, position, model, treeiter) = self.get_current_file()
        if (element == None):
            return

        ask_w = devede.ask.ask_window(self.config)
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

        element.properties(model,treeiter)

    def on_adjust_disc_usage_clicked(self,b):

        pass



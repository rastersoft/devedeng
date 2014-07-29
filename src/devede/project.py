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
import devede.message
import devede.dvd_menu
import devede.create_disk_window
import devede.runner
import devede.settings

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

    def on_adjust_disc_usage_clicked(self,b):

        pass

    def on_menu_options_clicked(self,b):

        self.menu.show_configuration(self.get_all_files())

    def on_create_disc_clicked(self,b):

        data = devede.create_disk_window.create_disk_window()
        if (not data.run()):
            return

        run_window = devede.runner.runner()
        file_movies = self.get_all_files()
        if (self.wcreate_menu.get_active()):
            processes,menu_entries = self.menu.create_dvd_menus(file_movies, data.path)
            for p in processes:
                run_window.add_process(p)
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
            counter += 1

        if (self.menu.at_startup == "menu_show_at_startup"):
            start_with_menu = True
        else:
            start_with_menu = False

        if (self.disc_type == "dvd"):
            self.create_dvdauthor_xml(data.path,file_movies,menu_entries, start_with_menu)

        run_window.connect("done",self.disc_done)
        self.wmain_window.hide()
        run_window.run()

    def expand_xml(self,text):

        text=text.replace('&','&amp;')
        text=text.replace('<','&lt;')
        text=text.replace('>','&gt;')
        text=text.replace('"','&quot;')
        text=text.replace("'",'&apos;')
        return text

    def create_dvdauthor_xml(self,movie_folder, file_movies, menu_entries, start_with_menu):

        xmlpath = os.path.join(movie_folder,"xml_data")
        datapath = os.path.join(movie_folder,"dvd_tree")
        try:
            os.makedirs(xmlpath)
        except:
            pass
        try:
            os.makedirs(datapath)
        except:
            pass

        if (len(file_movies) == 1) and (menu_entries == None):
            onlyone = True
        else:
            onlyone = False

        if (menu_entries == None):
            elements_per_menu = 1000
        else:
            elements_per_menu = len(menu_entries[0]["chapters"])

        xml_file=open(os.path.join(xmlpath,"dvdauthor.xml"),"w")
        xml_file.write('<dvdauthor dest="'+datapath+'">\n')

        if onlyone:
            xml_file.write('\t<vmgm />\n')
        else:
            xml_file.write('\t<vmgm>\n')

            # MENU

            # in the FPC we do a jump to the first menu in the first titleset if we wanted MENU
            # or we jump to the second titleset if we didn't want MENU at startup

            xml_file.write('\t\t<fpc>\n')
            xml_file.write('\t\t\tg0=100;\n')
            if (menu_entries != None) and (start_with_menu):
                xml_file.write('\t\t\tg1=0;\n')
            else:
                xml_file.write('\t\t\tg1=100;\n')
            xml_file.write('\t\t\tg2=1024;\n')
            xml_file.write('\t\t\tjump menu 1;\n')
            xml_file.write('\t\t</fpc>\n')


            # in the VMGM menu we create a code to jump to the title specified in G0
            # but if the title is 100, we jump to the menus. There we show the menu number
            # contained in G1

            xml_file.write("\t\t<menus>\n")

            xml_file.write('\t\t\t<video format="')
            if self.config.PAL:
                xml_file.write("pal")
            else:
                xml_file.write("ntsc")
            xml_file.write('" aspect="4:3"> </video>\n')

            xml_file.write('\t\t\t<pgc>\n')
            xml_file.write('\t\t\t\t<pre>\n')

            counter=1
            for element in file_movies:
                xml_file.write('\t\t\t\t\tif (g0 eq '+str(counter)+') {\n')
                xml_file.write('\t\t\t\t\t\tjump titleset '+str(1+counter)+' menu;\n')
                xml_file.write('\t\t\t\t\t}\n')
                counter+=1
            xml_file.write('\t\t\t\t\tif (g0 eq 100) {\n')
            xml_file.write('\t\t\t\t\t\tg2=1024;\n')
            xml_file.write('\t\t\t\t\t\tjump titleset 1 menu;\n')
            xml_file.write('\t\t\t\t\t}\n')
            xml_file.write('\t\t\t\t</pre>\n')
            # fake video (one black picture with one second of sound) to ensure 100% compatibility
            xml_file.write('\t\t\t\t<vob file="')

            if self.config.PAL:
                xml_file.write(self.expand_xml(str(os.path.join(self.config.other_path,"base_pal.mpg"))))
            else:
                xml_file.write(self.expand_xml(str(os.path.join(self.config.other_path,"base_ntsc.mpg"))))

            xml_file.write('"></vob>\n')
            xml_file.write('\t\t\t</pgc>\n')
            xml_file.write('\t\t</menus>\n')
            xml_file.write("\t</vmgm>\n")

            xml_file.write("\n")


            # the first titleset contains all the menus. G1 allows us to jump to the desired menu

            xml_file.write('\t<titleset>\n')
            xml_file.write('\t\t<menus>\n')
            xml_file.write('\t\t\t<video format="')
            if self.config.PAL:
                xml_file.write("pal")
            else:
                xml_file.write("ntsc")
            xml_file.write('" aspect="4:3"> </video>\n')

            first_entry = True
            menu_number = 0

            counter = 1
            title_list = []
            for element in file_movies:
                if element.show_in_menu:
                    title_list.append(counter)
                counter += 1

            if (menu_entries != None):
                nmenues = len(menu_entries)
                button_counter = 0
                for menu_page in menu_entries:
                    xml_file.write('\t\t\t<pgc>\n')
                    xml_file.write('\t\t\t\t<pre>\n')
                    # first we recover the currently selected button
                    xml_file.write('\t\t\t\t\ts8=g2;\n')

                    if first_entry: # here we add some code to jump to each menu
                        for menu2 in range(nmenues-1):
                            xml_file.write('\t\t\t\t\tif (g1 eq '+str(menu2+1)+') {\n')
                            xml_file.write('\t\t\t\t\t\tjump menu '+str(menu2+2)+';\n')
                            xml_file.write('\t\t\t\t\t}\n')

                        # this code is to fix a bug in some players
                        xml_file.write('\t\t\t\t\tif (g1 eq 100) {\n')
                        xml_file.write('\t\t\t\t\t\tjump title 1;\n') #menu '+str(self.nmenues+1)+';\n')
                        xml_file.write('\t\t\t\t\t}\n')
                    first_entry = False

                    xml_file.write('\t\t\t\t</pre>\n')
                    xml_file.write('\t\t\t\t<vob file="')

                    xml_file.write(self.expand_xml(menu_page["filename"]))
                    xml_file.write('></vob>\n')

                    for nbutton in menu_page["chapters"]:
                        xml_file.write('\t\t\t\t<button name="'+nbutton+'"> g0='+str(title_list[button_counter])+'; jump vmgm menu; </button>\n')
                        button_counter+=1

                    if (menu_page["left"] != None):
                        xml_file.write('\t\t\t\t<button name="'+menu_page["left"]+'p"> g1=')
                        xml_file.write(str(menu_number-1))
                        xml_file.write('; g2=1024; jump menu ')
                        xml_file.write(str(menu_number))
                        xml_file.write('; </button>\n')

                    if (menu_page["right"] != None):
                        xml_file.write('\t\t\t\t<button name="'+menu_page["right"]+'n"> g1=')
                        xml_file.write(str(menu_number+1))
                        xml_file.write('; g2=1024; jump menu ')
                        xml_file.write(str(menu_number+2))
                        xml_file.write('; </button>\n')

                    xml_file.write('\t\t\t\t<post>\n')
                    xml_file.write('\t\t\t\t\tg2=s8;\n')
                    xml_file.write('\t\t\t\t\tg1='+str(menu_number)+';\n')
                    xml_file.write('\t\t\t\t\tjump menu '+str(menu_number+1)+';\n')
                    xml_file.write('\t\t\t\t</post>\n')
                    xml_file.write('\t\t\t</pgc>\n')
                    menu_number += 1

                xml_file.write('\t\t</menus>\n')
            else:
                xml_file.write('\t\t\t<pgc>\n')
                xml_file.write('\t\t\t\t<pre>\n')
                # first we recover the currently selected button
                xml_file.write('\t\t\t\t\ts8=g2;\n')

                # this code is to fix a bug in some players
                xml_file.write('\t\t\t\t\tif (g1 eq 100) {\n')
                xml_file.write('\t\t\t\t\t\tjump title 1;\n') #menu '+str(self.nmenues+1)+';\n')
                xml_file.write('\t\t\t\t\t}\n')

                xml_file.write('\t\t\t\t</pre>\n')
                xml_file.write('\t\t\t\t<vob file="')
                if self.config.PAL:
                    xml_file.write(self.expand_xml(str(os.path.join(self.config.other_path,"base_pal.mpg")))+'"')
                else:
                    xml_file.write(self.expand_xml(str(os.path.join(self.config.other_path,"base_ntsc.mpg")))+'"')
                xml_file.write('></vob>\n')

                xml_file.write('\t\t\t\t<post>\n')
                xml_file.write('\t\t\t\t\tg2=s8;\n')
                xml_file.write('\t\t\t\t\tg1=0;\n')
                xml_file.write('\t\t\t\t\tjump menu 1;\n')
                xml_file.write('\t\t\t\t</post>\n')
                xml_file.write('\t\t\t</pgc>\n')

                xml_file.write('\t\t</menus>\n')

            xml_file.write('\t\t<titles>\n')
            xml_file.write('\t\t\t<video format="')
            if self.config.PAL:
                xml_file.write("pal")
            else:
                xml_file.write("ntsc")
            xml_file.write('" aspect="4:3"> </video>\n')
            xml_file.write('\t\t\t<pgc>\n')
            xml_file.write('\t\t\t\t<vob file="')
            if self.config.PAL:
                xml_file.write(self.expand_xml(str(os.path.join(self.config.other_path,"base_pal.mpg"))))
            else:
                xml_file.write(self.expand_xml(str(os.path.join(self.config.other_path,"base_ntsc.mpg"))))
            xml_file.write('"></vob>\n')
            xml_file.write('\t\t\t\t<post>\n')
            xml_file.write('\t\t\t\t\tg0=1;\n')
            xml_file.write('\t\t\t\t\tg1=0;\n')
            xml_file.write('\t\t\t\t\tg2=1024;\n')
            xml_file.write('\t\t\t\t\tcall vmgm menu entry title;\n')
            xml_file.write('\t\t\t\t</post>\n')
            xml_file.write('\t\t\t</pgc>\n')
            xml_file.write('\t\t</titles>\n')
            xml_file.write("\t</titleset>\n")

            xml_file.write("\n")


        # Now, create the titleset for each video

        total_t=len(file_movies)
        titleset=1
        titles=0
        counter=0
        for element in file_movies:
            files=0
            action=element.actions

            xml_file.write("\n")

            if element.is_mpeg_ps:

                # if it's already an MPEG-2 compliant file, we use the original values
                if element.original_fps == 25:
                    pal_ntsc="pal"
                    ispal=True
                else:
                    pal_ntsc="ntsc"
                    ispal=False

                if element.original_aspect_ratio > 1.6:
                    faspect='16:9'
                    fwide=True
                else:
                    faspect='4:3'
                    fwide=False

            else:
                # but if we are converting it, we use the desired values
                if element.format_pal:
                    pal_ntsc="pal"
                    ispal=True
                else:
                    pal_ntsc="ntsc"
                    ispal=False

                if element.aspect_ratio_final > 1.6:
                    faspect='16:9'
                    fwide=True
                else:
                    faspect='4:3'
                    fwide=False

            xml_file.write("\t<titleset>\n")

            if not onlyone:
                xml_file.write("\t\t<menus>\n")
                xml_file.write('\t\t\t<video format="'+pal_ntsc+'" aspect="'+faspect+'"')
                if fwide:
                    xml_file.write(' widescreen="nopanscan"')
                xml_file.write('> </video>\n')

                xml_file.write("\t\t\t<pgc>\n")
                xml_file.write("\t\t\t\t<pre>\n")
                xml_file.write('\t\t\t\t\tif (g0 eq 100) {\n')
                xml_file.write('\t\t\t\t\t\tjump vmgm menu entry title;\n')
                xml_file.write('\t\t\t\t\t}\n')
                xml_file.write('\t\t\t\t\tg0=100;\n')
                xml_file.write('\t\t\t\t\tg1='+str(int(titles/elements_per_menu))+';\n')
                xml_file.write('\t\t\t\t\tjump title 1;\n')
                xml_file.write('\t\t\t\t</pre>\n')
                # fake video to ensure compatibility
                xml_file.write('\t\t\t\t<vob file="')
                if ispal:
                    xml_file.write(self.expand_xml(str(os.path.join(self.config.other_path,"base_pal"))))
                else:
                    xml_file.write(self.expand_xml(str(os.path.join(self.config.other_path,"base_ntsc"))))
                if fwide:
                    xml_file.write("_wide")
                xml_file.write('.mpg"></vob>\n')
                xml_file.write("\t\t\t</pgc>\n")
                xml_file.write("\t\t</menus>\n")

            xml_file.write("\t\t<titles>\n")
            xml_file.write('\t\t\t<video format="'+pal_ntsc+'" aspect="'+faspect+'"')
            if fwide:
                xml_file.write(' widescreen="nopanscan"')
            xml_file.write('> </video>\n')

#             subtitles part
#             for element3 in element2["sub_list"]:
#                 xml_file.write('\t\t\t<subpicture lang="'+self.expand_xml(str(element3["sub_language"][:2].lower()))+'" />\n')
            xml_file.write('\t\t\t<pgc>\n')

#             if (element2["force_subs"]) and (len(element2["sub_list"])!=0):
#                 xml_file.write('\t\t\t\t<pre>\n')
#                 xml_file.write('\t\t\t\t\tsubtitle=64;\n')
#                 xml_file.write('\t\t\t\t</pre>\n')

            xml_file.write('\t\t\t\t<vob file="'+self.expand_xml(element.converted_filename)+'" ')
            xml_file.write('chapters="0')
            if (element.original_length > 5):
                if (element.divide_in_chapters): # add chapters
                    toadd = element.chapter_size
                    seconds = toadd*60
                    while seconds < (element.original_length - 4):
                        thetime = self.return_time(seconds,False)
                        xml_file.write(","+thetime)
                        seconds += (toadd*60)
                xml_file.write(',' + self.return_time((element.original_length -2 ),False))
            xml_file.write('" />\n')

            if not onlyone:
                xml_file.write('\t\t\t\t<post>\n')
                files+=1
                xml_file.write('\t\t\t\t\tg1='+str(int(titles/elements_per_menu))+';\n')
                if (action=="action_stop"):
                    xml_file.write('\t\t\t\t\tg0=100;\n')
                    xml_file.write('\t\t\t\t\tcall vmgm menu entry title;\n')
                else:
                    xml_file.write('\t\t\t\t\tg0=')
                    if action=="action_play_previous":
                        if titles == 0:
                            prev_t = total_t - 1
                        else:
                            prev_t = titles - 1
                        xml_file.write(str(title_list[prev_t]))
                    elif action=="action_play_again":
                        xml_file.write(str(title_list[titles]))
                    elif action=="action_play_next":
                        if titles==total_t-1:
                            next_t=0
                        else:
                            next_t=titles+1
                        xml_file.write(str(title_list[next_t]))
                    elif action=="action_play_last":
                        xml_file.write(str(title_list[total_t-1]))
                    else:
                        xml_file.write('1') # first

                    xml_file.write(';\n')
                    xml_file.write('\t\t\t\t\tcall vmgm menu entry title;\n')
                xml_file.write('\t\t\t\t</post>\n')
            xml_file.write("\t\t\t</pgc>\n")
            xml_file.write("\t\t</titles>\n")
            xml_file.write("\t</titleset>\n")
            counter+=1
            titles+=1

        xml_file.write("</dvdauthor>")

        xml_file.close()


    def return_time(self,seconds,empty):

        """ cuts a time in seconds into seconds, minutes and hours """

        seconds2=int(seconds)

        hours=str(int(seconds2/3600))
        if empty:
            if len(hours)==1:
                hours="0"+hours
        else:
            if hours=="0":
                hours=""
        if hours!="":
            hours+=":"

        minutes=str(int((seconds2/60)%60))
        if empty or (hours!=""):
            if len(minutes)==1:
                minutes="0"+minutes
        elif (minutes=="0") and (hours==""):
                minutes=""
        if minutes!="":
            minutes+=":"

        secs=str(int(seconds2%60))
        if (len(secs)==1) and (minutes!=""):
            secs="0"+secs

        return hours+minutes+secs


    def disc_done(self,object,value):

        self.wmain_window.show()

    def on_preview_file_clicked(self,b):

        (element, position, model, treeiter) = self.get_current_file()
        if (element == None):
            return
        element.do_preview()

    def on_settings_activate(self,b):

        w = devede.settings.settings_window()
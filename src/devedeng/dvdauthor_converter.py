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

import os
import devedeng.configuration_data
import devedeng.executor

class dvdauthor_converter(devedeng.executor.executor):

    def __init__(self):

        devedeng.executor.executor.__init__(self)
        self.config = devedeng.configuration_data.configuration.get_config()


    def create_dvd_project (self, path, name, file_movies, menu_entries, start_with_menu, play_all_opt):

        movie_path = os.path.join(path,"dvd_tree")
        try:
            os.makedirs(movie_path)
        except:
            pass

        xml_file = self.create_dvdauthor_xml(path, file_movies, menu_entries, start_with_menu, play_all_opt)

        self.command_var=[]
        self.command_var.append("dvdauthor")
        self.command_var.append("-o")
        self.command_var.append(movie_path)
        self.command_var.append("-x")
        self.command_var.append(xml_file)
        self.use_pulse_mode = True
        self.text = _("Creating DVD structure")


    def process_stdout(self,data):
        return


    def process_stderr(self,data):
        if (data != None) and (data[0] != ""):
            self.progress_bar[1].set_text(data[0])
        return


    def create_dvdauthor_xml(self,movie_folder, file_movies, menu_entries, start_with_menu, play_all_opt):

        xmlpath = os.path.join(movie_folder,"xml_data")
        xml_file_path = os.path.join(xmlpath,"dvdauthor.xml")
        datapath = os.path.join(movie_folder,"dvd_tree")
        try:
            os.makedirs(xmlpath)
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

        xml_file=open(xml_file_path,"w")
        xml_file.write('<dvdauthor dest="'+datapath+'">\n')

        if onlyone:
            xml_file.write('\t<vmgm>\n')
            xml_file.write("\t\t<menus>\n")

            xml_file.write('\t\t\t<video format="')
            if self.config.PAL:
                xml_file.write("pal")
            else:
                xml_file.write("ntsc")
            xml_file.write('" aspect="4:3"> </video>\n')
            xml_file.write("\t\t</menus>\n")
            xml_file.write('\t</vmgm>\n')
        else:
            xml_file.write('\t<vmgm>\n')

            # MENU

            # in the FPC we do a jump to the first menu in the first titleset if we wanted MENU
            # or we jump to the second titleset if we didn't want MENU at startup

            xml_file.write('\t\t<fpc>\n')
            xml_file.write('\t\t\tg0=100;\n')
            xml_file.write('\t\t\tg1=') #goto variable
            if (menu_entries != None) and (start_with_menu):
                xml_file.write('0;\n') #show menu
            else:
                xml_file.write('100;\n') #auto play
            xml_file.write('\t\t\tg2=1024;\n') #highlight?
            xml_file.write('\t\t\tg3=') #play all variable
            if play_all_opt and (menu_entries != None) and (start_with_menu):
                xml_file.write('1;\n') #auto play all
            else:
                xml_file.write('0;\n') #do not play all
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
                    xml_file.write('\t\t\t\t\ts8=g2;\n') # first we recover the currently selected button
                    xml_file.write('\t\t\t\t\tg3=0;\n') #turnoff play all

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
                    xml_file.write('"></vob>\n')

                    for nbutton in menu_page["chapters"]:
                        #xml_file.write('\t\t\t\t<button name="'+nbutton+'"> g0='+str(title_list[button_counter])+'; jump vmgm menu; </button>\n')
                        xml_file.write('\t\t\t\t<button name="'+nbutton+'">\n')
                        xml_file.write('\t\t\t\t\tg0='+str(title_list[button_counter])+';\n')
                        if play_all_opt and nbutton == "boton0x0":
                            xml_file.write('\t\t\t\t\tg3=1;\n')
                        xml_file.write('\t\t\t\t\tjump vmgm menu;\n')
                        xml_file.write('\t\t\t\t</button>\n')
                        if not play_all_opt:
                            button_counter+=1

                    if (menu_page["left"] != None):
                        xml_file.write('\t\t\t\t<button name="'+menu_page["left"]+'"> g1=')
                        xml_file.write(str(menu_number-1))
                        xml_file.write('; g2=1024; jump menu ')
                        xml_file.write(str(menu_number))
                        xml_file.write('; </button>\n')

                    if (menu_page["right"] != None):
                        xml_file.write('\t\t\t\t<button name="'+menu_page["right"]+'"> g1=')
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
                    xml_file.write(self.expand_xml(str(os.path.join(self.config.other_path,"base_pal.mpg"))))
                else:
                    xml_file.write(self.expand_xml(str(os.path.join(self.config.other_path,"base_ntsc.mpg"))))
                xml_file.write('"></vob>\n')

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
                    manual_chapter_list = [];
                    if (element.chapter_list_entry):
                        manual_chapter_list = element.chapter_list_entry.split(",")
                    toadd = element.chapter_size
                    seconds = toadd*60
                    while seconds < (element.original_length - 4):
                        # Check manual_chapter_list for manual entries before set next chapter
                        for idx, m_chapter in enumerate(manual_chapter_list):
                            m_chapter = m_chapter.split(":")
                            m_chapter = int(m_chapter[0])*60+int(m_chapter[1]) # Change from mm:ss to seconds
                            if (m_chapter < seconds):
                                seconds = m_chapter
                                del manual_chapter_list[idx]
                        thetime = self.return_time(seconds,False)
                        xml_file.write(","+thetime)
                        seconds += (toadd*60)
                xml_file.write(',' + self.return_time((element.original_length -2 ),False))
            xml_file.write('" />\n')

            if not onlyone:
                xml_file.write('\t\t\t\t<post>\n')
                files+=1
                xml_file.write('\t\t\t\t\tg1='+str(int(titles/elements_per_menu))+';\n')

                #play all
                xml_file.write('\t\t\t\t\tif (g3 eq 1) {\n') #if play all:
                if titles==total_t-1: #return to menu if last title
                    xml_file.write('\t\t\t\t\t\tg0=100;\n')
                else: #play next title
                    xml_file.write('\t\t\t\t\t\tg0='+str(titles + 2)+';\n')
                xml_file.write('\t\t\t\t\t} else {\n')

                #end of play opt
                xml_file.write('\t\t\t\t\t\tg0=')
                if action=="action_stop":
                    xml_file.write('100')
                elif action=="action_play_previous":
                    if titles == 0:
                        prev_t = total_t - 1
                    else:
                        prev_t = titles - 1
                    xml_file.write(str(prev_t + 1))
                elif action=="action_play_again":
                    xml_file.write(str(titles + 1))
                elif action=="action_play_next":
                    if titles==total_t-1:
                        next_t=0
                    else:
                        next_t=titles + 1
                    xml_file.write(str(next_t + 1))
                elif action=="action_play_last":
                    xml_file.write(str(total_t))
                else:
                    xml_file.write('1') # first

                xml_file.write(';\n')
                xml_file.write('\t\t\t\t\t}\n')

                xml_file.write('\t\t\t\t\tcall vmgm menu entry title;\n') #preform action
                xml_file.write('\t\t\t\t</post>\n')
            xml_file.write("\t\t\t</pgc>\n")
            xml_file.write("\t\t</titles>\n")
            xml_file.write("\t</titleset>\n")
            counter+=1
            titles+=1

        xml_file.write("</dvdauthor>")

        xml_file.close()

        return xml_file_path


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

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
import devedeng.configuration_data
import devedeng.add_files


class ask_subtitles:

    def __init__(self):

        self.config = devedeng.configuration_data.configuration.get_config()

    def run(self):

        builder = Gtk.Builder()
        builder.set_translation_domain(self.config.gettext_domain)

        builder.add_from_file(os.path.join(
            self.config.glade, "wask_subtitles.ui"))
        builder.connect_signals(self)
        wask_window = builder.get_object("ask_subtitles")
        self.wfilename = builder.get_object("subtitle_file")
        self.waccept = builder.get_object("accept")
        wlist_encodings = builder.get_object("list_encodings")
        wlist_languages = builder.get_object("list_languages")
        wencoding = builder.get_object("encoding_l")
        wlanguage = builder.get_object("language_l")

        if (devedeng.add_files.add_files.last_path is not None):
            self.wfilename.set_current_folder(
                devedeng.add_files.add_files.last_path)

        lang_selection = 0
        enc_selection = 0

        self.language = None
        self.encoding = None
        self.put_upper = False
        self.filename = None

        counter = 0
        encodings = open(os.path.join(self.config.other_path, "codepages.lst"))
        for element in encodings:
            element = element.strip()
            if (element == self.config.sub_codepage):
                enc_selection = counter
            wlist_encodings.append([element])
            counter += 1
        encodings.close()

        counter = 0
        languages = open(os.path.join(self.config.other_path, "languages.lst"))
        for element in languages:
            element = element.strip()
            if (element == self.config.sub_language):
                lang_selection = counter
            wlist_languages.append([element])
            counter += 1
        languages.close()

        wencoding.set_active(enc_selection)
        wlanguage.set_active(lang_selection)

        file_filter_subt = Gtk.FileFilter()
        file_filter_subt.set_name(_("Subtitle files"))

        file_filter_subt.add_pattern("*.sub")
        file_filter_subt.add_pattern("*.srt")
        file_filter_subt.add_pattern("*.ssa")
        file_filter_subt.add_pattern("*.smi")
        file_filter_subt.add_pattern("*.rt")
        file_filter_subt.add_pattern("*.txt")
        file_filter_subt.add_pattern("*.aqt")

        file_filter_all = Gtk.FileFilter()
        file_filter_all.set_name(_("All files"))
        file_filter_all.add_pattern("*")

        self.wfilename.add_filter(file_filter_subt)
        self.wfilename.add_filter(file_filter_all)

        wask_window.show_all()
        self.on_subtitle_file_set(None)
        retval = wask_window.run()
        if (retval == 2):  # accept
            self.put_upper = builder.get_object(
                "put_subtitles_upper").get_active()
            self.config.sub_codepage = wencoding.get_active_id()
            self.config.sub_language = wlanguage.get_active_id()
            self.encoding = wencoding.get_active_id()
            self.language = wlanguage.get_active_id()[:2]
            self.filename = self.wfilename.get_filename()

        wask_window.destroy()
        if (retval == 2):
            return True
        else:
            return False

    def on_subtitle_file_set(self, b):

        f = self.wfilename.get_filename()
        if (f is None) or (f == ""):
            self.waccept.set_sensitive(False)
        else:
            self.waccept.set_sensitive(True)

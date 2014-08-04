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
import devede.error
import devede.ask

class runner(GObject.GObject):

    __gsignals__ = {'done': (GObject.SIGNAL_RUN_FIRST, None,(int,))}

    def __init__(self, show_window = True):

        GObject.GObject.__init__(self)

        self.config = devede.configuration_data.configuration.get_config()

        if (self.config.multicore > 0):
            if self.config.cores < self.config.multicore:
                self.cores = self.config.cores
            else:
                self.cores = self.config.multicore
        else:
            self.cores = self.config.cores - self.config.multicore
            if (self.cores <= 0):
                self.cores = 1

        self.proc_list = []
        self.running = 0

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(self.config.gettext_domain)

        self.builder.add_from_file(os.path.join(self.config.glade,"wprogress.ui"))
        self.builder.connect_signals(self)
        self.wprogress = self.builder.get_object("progress")
        if show_window:
            self.wprogress.show_all()
        self.wtotal = self.builder.get_object("progress_total")

        progress_frame = self.builder.get_object("progress_frame")
        box = Gtk.Box(Gtk.Orientation.VERTICAL, 0)
        progress_frame.add(box)
        box.show()
        self.progress_bars = []
        self.used_progress_bars = []
        for c in range(0,self.cores):
            f = Gtk.Frame()
            p = Gtk.ProgressBar()
            p.set_orientation(Gtk.Orientation.HORIZONTAL)
            p.set_show_text(True)
            f.add(p)
            # A frame, a progress bar, and the process running in that bar
            self.progress_bars.append([f, p, None])
            box.pack_start(f,True,True,0)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        self.total_processes = 0
        self.error = False


    def add_process(self,process):

        if (self.proc_list.count(process) == 0):
            self.proc_list.append(process)

        for p in process.childs:
            self.add_process(p)

        self.total_processes = len(self.proc_list)


    def on_cancel_clicked(self,b):

        ask_w = devede.ask.ask_window()
        retval = ask_w.run(_("Cancel the current job?"),_("Cancel the current job?"))
        if retval:
            self.error = True
            for element in self.proc_list:
                element.cancel()
            self.wprogress.destroy()
            self.emit("done",1) # there was an error
            return

    def run(self, clear_log = True):

        if clear_log:
            self.config.clear_log()

        for element in self.proc_list:
            # each element has three items:
            # * the process object
            # * the list of dependencies, or None if there are no more dependencies
            # * the progress bar being used by this process
            if (element.dependencies == None) and (element.progress_bar == None):
                element.connect("ended",self.process_ended)
                element.run(self.progress_bars[0])
                element.progress_bar = self.progress_bars[0]
                self.used_progress_bars.append(self.progress_bars[0])
                if (len(self.progress_bars) > 1):
                    self.progress_bars = self.progress_bars[1:]
                else:
                    self.progress_bars = []
                    break
        self.wtotal.set_text(str(self.total_processes - len(self.proc_list))+"/"+str(self.total_processes))
        self.wtotal.set_fraction((float(self.total_processes - len(self.proc_list)))/(float(self.total_processes)))


    def process_ended(self,process, retval):

        if self.error:
            return

        if retval != 0:
            self.error = True
            for element in self.proc_list:
                element.cancel()
            self.wprogress.destroy()
            devede.error.error_window()
            self.emit("done",1) # there was an error
            return

        # move the progress bar used by this process to the list of available progress bars
        tmp = []
        for e in self.used_progress_bars:
            if (process.progress_bar == e):
                self.progress_bars.append(e)
                e[0].hide()
            else:
                tmp.append(e)
        self.used_progress_bars = tmp

        # remove this process from the list of processes, and remove it from the dependencies in other processes
        tmp = []
        for e in self.proc_list:
            if (e != process):
                tmp.append(e)
                e.remove_dependency(process)
        self.proc_list = tmp

        # launch a new process
        if (len(self.proc_list) != 0):
            self.run(False)
        else:
            self.wprogress.destroy()
            self.emit("done",0) # no error
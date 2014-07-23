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

from gi.repository import GLib,GObject
import subprocess
import os
import signal
import devede.configuration_data

class executor(GObject.GObject):
    """ This class encapsulates everything needed for launching processes """

    __gsignals__ = {'ended': (GObject.SIGNAL_RUN_FIRST, None,(int,))}

    def __init__(self):

        GObject.GObject.__init__(self)

        self.config = devede.configuration_data.configuration.get_config()
        self.channel_stdout = None
        self.channel_stderr = None
        self.text = ""
        self.stdout_data = ""
        self.stderr_data = ""

    def run(self, progress_bar):

        self.progress_bar = progress_bar
        self.launch_process(self.command_var)
        self.progress_bar[0].set_label(self.text)
        self.progress_bar[1].set_fraction(0.0)
        self.progress_bar[0].show_all()

    def remove_ansi(self,line):

        output=""
        while True:
            pos=line.find("\033[") # try with double-byte ESC
            jump=2
            if pos==-1:
                pos=line.find("\233") # if not, try with single-byte ESC
                jump=1
            if pos==-1: # no ANSI characters; we ended
                output+=line
                break

            output+=line[:pos]
            line=line[pos+jump:]

            while True:
                if len(line)==0:
                    break
                if (ord(line[0])<64) or (ord(line[0])>126):
                    line=line[1:]
                else:
                    line=line[1:]
                    break
        return output


    def launch_process(self,command):

        self.config.append_log("Launching:",False)
        for e in command:
            self.config.append_log(e+" ")

        self.handle = subprocess.Popen(command,stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        self.channel_stdout = GLib.IOChannel(self.handle.stdout.fileno())
        self.channel_stderr = GLib.IOChannel(self.handle.stderr.fileno())
        self.channel_stdout.add_watch(GLib.IO_IN | GLib.IO_HUP,self.read_stdout)
        self.channel_stderr.add_watch(GLib.IO_IN | GLib.IO_HUP,self.read_stderr)
        self.stdout_buf = ""
        self.stderr_buf = ""

    def read_stdout(self,source,condition):

        if (condition != GLib.IO_IN):
            self.channel_stdout = None
            if (self.channel_stderr == None):
                self.wait_end()
            return False
        else:
            line_data = self.stdout_buf+(self.handle.stdout.read1(4096).decode("utf-8"))
            self.stdout_data += line_data
            data = (line_data).replace("\r","\n").split("\n")
            if (len(data) == 1):
                final_data = []
                self.stdout_buf = data[0]
            else:
                final_data = data[:-1]
                self.stdout_buf = data[-1]
            if (len(final_data) != 0):
                self.process_stdout(final_data)
            return True

    def read_stderr(self,source,condition):

        if (condition != GLib.IO_IN):
            self.channel_stderr = None
            if (self.channel_stdout == None):
                self.wait_end()
            return False
        else:
            line_data = self.stderr_buf+(self.handle.stderr.read1(4096).decode("utf-8"))
            self.stderr_data += line_data
            data = (line_data).replace("\r","\n").split("\n")
            if (len(data) == 1):
                final_data = []
                self.stderr_buf = data[0]
            else:
                final_data = data[:-1]
                self.stderr_buf = data[-1]
            if (len(final_data) != 0):
                self.process_stderr(final_data)
            return True

    def cancel(self):

        """ Called to kill this process. """

        if self.handle==None:
            return
        os.kill(self.handle.pid,signal.SIGKILL)


    def wait_end(self):

        self.config.append_log(self.text)
        self.config.append_log(self.stdout_data)
        self.config.append_log(self.stderr_data)
        retval = self.handle.wait()
        self.emit("ended",retval)
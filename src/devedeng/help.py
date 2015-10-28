#!/usr/bin/env python3

from gi.repository import Gtk,Gdk
import devedeng.configuration_data
import os

class help:
    
    def __init__(self,help_page):

        self.config = devedeng.configuration_data.configuration.get_config()

        file="file://"+os.path.join(self.config.help_path,"html",help_page)

        retval = Gtk.show_uri(None,file,Gdk.CURRENT_TIME)
        if retval == False:
            msg=devede_dialogs.show_error(gladefile,_("Can't open the help files."))

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

from gi.repository import GObject

class interface_manager(GObject.GObject):
    """ This class allows to automatically generate variables for a GLADE interface,
        set the widgets in the interface to their values, and copy the current values
        in the widgets to the variables """

    def __init__(self):

        self.interface_groups = {}
        self.interface_toggles = []
        self.interface_labels = []
        self.interface_text = []
        self.interface_show_hide = []
        self.interface_enable_disable = []
        self.interface_float_adjustments = []
        self.interface_integer_adjustments = []
        self.interface_lists = []

    def add_group(self,group_name,radiobutton_list,default_value):
        """ Adds a group of radiobuttons and creates an internal variable with
            the name group_name, setting it to default_value. The
            value for the variable will be the name of the active
            radiobutton """

        if (default_value != None):
            exec('self.'+group_name+' = "'+str(default_value)+'"')
        else:
            exec('self.'+group_name+' = None')
        self.interface_groups[group_name] = radiobutton_list

    def add_toggle(self,toggle_name,default_value):
        """ Adds an internal variable with the name toggle_name, linked to a widget
            element with the same name (must be or inherint from Gtk.ToogleButton).
            The default value can be True of False """

        exec('self.'+toggle_name+' = '+str(default_value))
        self.interface_toggles.append(toggle_name)

    def add_text(self,text_name,default_value):
        """ Adds an internal variable with the name text_name, linked to an
            element with the same name (must be a Gtk.TextEntry or a Gtk.Label).
            The default value can be a text or None """

        if (default_value != None):
            exec('self.'+text_name+' = "'+str(default_value)+'"')
        else:
            exec('self.'+text_name+' = None')
        self.interface_text.append(text_name)

    def add_label(self,text_name,default_value):
        """ Adds an internal variable with the name text_name, linked to an
            element with the same name (must be a Gtk.TextEntry or a Gtk.Label).
            The default value can be a text or None. This element is copied to the UI,
            but is never updated from the UI if the user changes it """

        exec('self.'+text_name+' = default_value')
        self.interface_labels.append(text_name)

    def add_integer_adjustment(self,adjustment_name,default_value):
        """ Adds an internal variable with the name text_name, linked to an
            element with the same name (must be a Gtk.Adjustment).
            The default value must be an integer """

        exec('self.'+adjustment_name+' = '+str(default_value))
        self.interface_integer_adjustments.append(adjustment_name)

    def add_float_adjustment(self,adjustment_name,default_value):
        """ Adds an internal variable with the name text_name, linked to an
            element with the same name (must be a Gtk.Adjustment).
            The default value must be an float """

        exec('self.'+adjustment_name+' = '+str(default_value))
        self.interface_float_adjustments.append(adjustment_name)

    def add_list(self,liststore_name):

        exec('self.'+liststore_name+' = []')
        self.interface_lists.append(liststore_name)

    def add_show_hide(self,element_name,to_show,to_hide):
        """ Adds an element that can be active or inactive, and two lists of elements.
            The first one contains elements that will be visible when the element is
            active, and invisible when it is inactive, and the second one contains
            elements that will be visible when the element is inactive, and
            invisible when the element is active """

        self.interface_show_hide.append([element_name, to_show, to_hide])

    def add_enable_disable(self,element_name,to_enable,to_disable):
        """ Adds an element that can be active or inactive, and two lists of elements.
            The first one contains elements that will be enabled when the element is
            active, and disabled when it is inactive, and the second one contains
            elements that will be enabled when the element is inactive, and
            disabled when the element is active """

        self.interface_enable_disable.append([element_name, to_enable, to_disable])

    def update_ui(self,builder):
        """ Sets the value of the widgets in base of the internal variables """

        for key in self.interface_groups:
            obj = eval('self.'+key)
            builder.get_object(obj).set_active(True)

        for element in self.interface_toggles:
            value = eval('self.'+element)
            builder.get_object(element).set_active(value)

        for element in self.interface_text:
            value = eval('self.'+element)
            if (value != None):
                builder.get_object(element).set_text(value)
            else:
                builder.get_object(element).set_text("")

        for element in self.interface_labels:
            value = eval('self.'+element)
            if (value != None):
                builder.get_object(element).set_text(str(value))
            else:
                builder.get_object(element).set_text("")

        for element in self.interface_integer_adjustments:
            value = eval('self.'+element)
            builder.get_object(element).set_value(float(value))

        for element in self.interface_float_adjustments:
            value = eval('self.'+element)
            builder.get_object(element).set_value(value)

        for element in self.interface_lists:
            obj = eval('self.'+element)
            the_liststore = builder.get_object(element)
            the_liststore.clear()
            for item in obj:
                the_liststore.append(item)

        self.interface_show_hide_obj = {}
        for element in self.interface_show_hide:
            obj = builder.get_object(element[0])
            to_show = []
            for e2 in element[1]:
                to_show.append(builder.get_object(e2))
            to_hide = []
            for e3 in element[2]:
                to_hide.append(builder.get_object(e3))
            self.interface_show_hide_obj[obj] = [to_show, to_hide]
            obj.connect('toggled',self.toggled_element)
            self.toggled_element(obj)

        self.interface_enable_disable_obj = {}
        for element in self.interface_enable_disable:
            obj = builder.get_object(element[0])
            to_enable = []
            for e2 in element[1]:
                to_enable.append(builder.get_object(e2))
            to_disable = []
            for e3 in element[2]:
                to_disable.append(builder.get_object(e3))
            self.interface_enable_disable_obj[obj] = [to_enable, to_disable]
            obj.connect('toggled',self.toggled_element2)
            self.toggled_element2(obj)

    def toggled_element(self,element):
        """ Wenever an element with 'hide' or 'show' needs is toggled, this callback is called """

        # First, show all items for each possible element
        for key in self.interface_show_hide_obj:
            to_show = self.interface_show_hide_obj[key][0]
            to_hide = self.interface_show_hide_obj[key][1]

            active = key.get_active()

            for item in to_show:
                if active:
                    item.show()

            for item in to_hide:
                if not active:
                    item.show()

        # And now, hide all items that must be hiden
        # This is done this way because this allows to have an item being hiden by
        # one widget, and being shown by another: in that case, it will be hiden always
        for key in self.interface_show_hide_obj:
            to_show = self.interface_show_hide_obj[key][0]
            to_hide = self.interface_show_hide_obj[key][1]

            active = key.get_active()

            for item in to_show:
                if not active:
                    item.hide()

            for item in to_hide:
                if active:
                    item.hide()


    def toggled_element2(self,element):
        """ Wenever an element with 'enable' or 'disable' needs is toggled, this callback is called """

        # First enable all items that must be enabled
        for key in self.interface_enable_disable_obj:
            to_enable = self.interface_enable_disable_obj[key][0]
            to_disable = self.interface_enable_disable_obj[key][1]

            active = key.get_active()
            if (active):
                for item in to_enable:
                    item.set_sensitive(True)
            else:
                for item in to_disable:
                    item.set_sensitive(True)

        # And now, disable all items that must be disabled
        # This is done this way because this allows to have an item being disabled by
        # one widget, and being enabled by another: in that case, it will be disabled always
        for key in self.interface_enable_disable_obj:
            to_enable = self.interface_enable_disable_obj[key][0]
            to_disable = self.interface_enable_disable_obj[key][1]

            active = key.get_active()
            if (not active):
                for item in to_enable:
                    item.set_sensitive(False)
            else:
                for item in to_disable:
                    item.set_sensitive(False)

    def store_ui(self,builder):
        """ Takes the values of the widgets and stores them in the internal variables """

        for key in self.interface_groups:
            for element in self.interface_groups[key]:
                obj = builder.get_object(element)
                if obj.get_active():
                    exec('self.'+key+' = "'+element+'"')
                    break

        for element in self.interface_toggles:
            obj = builder.get_object(element)
            if obj.get_active():
                exec('self.'+element+' = True')
            else:
                exec('self.'+element+' = False')

        for element in self.interface_text:
            obj = builder.get_object(element)
            exec('self.'+element+' = obj.get_text()')

        for element in self.interface_integer_adjustments:
            obj = builder.get_object(element)
            exec('self.'+element+' = int(obj.get_value())')

        for element in self.interface_float_adjustments:
            obj = builder.get_object(element)
            exec('self.'+element+' = obj.get_value()')

        for element in self.interface_lists:
            exec('self.'+element+' = []')
            the_liststore = builder.get_object(element)
            ncolumns = the_liststore.get_n_columns()
            for row in the_liststore:
                final_row = []
                for c in range(0,ncolumns):
                    final_row.append(row.model[row.iter][c])
                print (final_row)
                exec('self.'+element+'.append(final_row)')
        
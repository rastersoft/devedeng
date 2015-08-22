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

from gi.repository import GObject,Gdk

class interface_manager(GObject.GObject):
    """ This class allows to automatically generate variables for a GLADE interface,
        set the widgets in the interface to their values, and copy the current values
        in the widgets to the variables """

    def __init__(self):

        GObject.GObject.__init__(self)
        self.interface_groups = {}
        self.interface_toggles = []
        self.interface_dualtoggles = []
        self.interface_labels = []
        self.interface_text = []
        self.interface_show_hide = []
        self.interface_enable_disable = []
        self.interface_float_adjustments = []
        self.interface_integer_adjustments = []
        self.interface_lists = []
        self.interface_colorbuttons = []
        self.interface_fontbuttons = []
        self.interface_filebuttons = []
        self.interface_comboboxes = []

    def add_group(self,group_name,radiobutton_list,default_value,callback = None):
        """ Adds a group of radiobuttons and creates an internal variable with
            the name group_name, setting it to default_value. The
            value for the variable will be the name of the active
            radiobutton """

        if (default_value != None):
            exec('self.'+group_name+' = "'+str(default_value)+'"')
        else:
            exec('self.'+group_name+' = None')
        self.interface_groups[group_name] = ( radiobutton_list, callback )

    def add_toggle(self,toggle_name,default_value,callback = None):
        """ Adds an internal variable with the name toggle_name, linked to a widget
            element with the same name (must be or inherint from Gtk.ToogleButton).
            The default value can be True of False """

        exec('self.'+toggle_name+' = '+str(default_value))
        self.interface_toggles.append( (toggle_name, callback) )

    def add_dualtoggle(self,toggle_name,toggle2,default_value,callback = None):
        """ Adds an internal variable with the name toggle_name, linked to widget
            elements with names toggle_nane and toggle2 (must be or inherint from Gtk.ToogleButton).
            The default value can be True of False, with True being toggle_name active, and False
            being toggle2 active """

        exec('self.'+toggle_name+' = '+str(default_value))
        self.interface_dualtoggles.append( (toggle_name, toggle2, callback) )

    def add_text(self,text_name,default_value,callback = None):
        """ Adds an internal variable with the name text_name, linked to an
            element with the same name (must be a Gtk.TextEntry or a Gtk.Label).
            The default value can be a text or None """

        if (default_value != None):
            exec('self.'+text_name+' = "'+str(default_value).replace('\"','\\"')+'"')
        else:
            exec('self.'+text_name+' = None')
        self.interface_text.append( (text_name, callback) )

    def add_label(self,text_name,default_value):
        """ Adds an internal variable with the name text_name, linked to an
            element with the same name (must be a Gtk.TextEntry or a Gtk.Label).
            The default value can be a text or None. This element is copied to the UI,
            but is never updated from the UI if the user changes it """

        exec('self.'+text_name+' = default_value')
        self.interface_labels.append(text_name)

    def add_integer_adjustment(self,adjustment_name,default_value,callback = None):
        """ Adds an internal variable with the name text_name, linked to an
            element with the same name (must be a Gtk.Adjustment).
            The default value must be an integer """

        exec('self.'+adjustment_name+' = '+str(default_value))
        self.interface_integer_adjustments.append( (adjustment_name, callback) )

    def add_float_adjustment(self,adjustment_name,default_value,callback = None):
        """ Adds an internal variable with the name text_name, linked to an
            element with the same name (must be a Gtk.Adjustment).
            The default value must be an float """

        exec('self.'+adjustment_name+' = '+str(default_value))
        self.interface_float_adjustments.append( (adjustment_name, callback))

    def add_list(self,liststore_name,callback = None):
        """ Adds an internal variable with the name liststore_name, linked to
            an element with the same name (must be a Gtk.ListStore). """

        exec('self.'+liststore_name+' = []')
        self.interface_lists.append( (liststore_name, callback ))

    def add_colorbutton(self,colorbutton_name, default_value,callback = None):
        """ Adds an internal variable with the name colorbutton_name, linked to an
            element with the same name (must be a Gtk.ColorButton).
            The default value must be a set with RGBA values """

        exec('self.'+colorbutton_name+' = default_value')
        self.interface_colorbuttons.append( (colorbutton_name, callback ))

    def add_fontbutton(self,fontbutton_name, default_value, callback = None):
        """ Adds an internal variable with the name fontbutton_name, linked to an
            element with the same name (must be a Gtk.FontButton).
            The default value must be a string with the font values """

        exec('self.'+fontbutton_name+' = default_value')
        self.interface_fontbuttons.append( (fontbutton_name, callback ))

    def add_filebutton(self,filebutton_name, default_value, callback = None):
        """ Adds an internal variable with the name filebutton_name, linked to an
            element with the same name (must be a Gtk.FileButton).
            The default value must be a string with the font values """

        exec('self.'+filebutton_name+' = default_value')
        self.interface_filebuttons.append( (filebutton_name, callback ) )

    def add_combobox(self,combobox_name,values,default_value,callback = None):
        """ Adds an internal variable with the name combobox_name, linked to an
            element with the same name (must be a Gtk.Combobox).
            The default value must be an integer with the entry selected """

        exec('self.'+combobox_name+' = default_value')
        self.interface_comboboxes.append ( (combobox_name, values, callback) )

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
            callback = self.interface_groups[key][1]
            if (callback != None):
                for element in self.interface_groups[key][0]:
                    obj = builder.get_object(element)
                    obj.connect("toggled",callback)

        for element in self.interface_toggles:
            value = eval('self.'+element[0])
            obj = builder.get_object(element[0])
            obj.set_active(value)
            callback = element[1]
            if (callback != None):
                obj.connect("toggled",callback)

        for element in self.interface_dualtoggles:
            value = eval('self.'+element[0])
            obj = builder.get_object(element[0])
            obj2 = builder.get_object(element[1])
            if value:
                obj.set_active(True)
            else:
                obj2.set_active(True)
            callback = element[2]
            if (callback != None):
                obj.connect("toggled",callback)

        for element in self.interface_text:
            value = eval('self.'+element[0])
            obj = builder.get_object(element[0])
            if (value != None):
                obj.set_text(value)
            else:
                obj.set_text("")
            callback = element[1]
            if (callback != None):
                obj.connect("changed",callback)

        for element in self.interface_labels:
            value = eval('self.'+element)
            obj = builder.get_object(element)
            if obj != None:
                if (value != None):
                    obj.set_text(str(value))
                else:
                    obj.set_text("")

        for element in self.interface_integer_adjustments:
            obj = builder.get_object(element[0])
            if obj != None:
                value = eval('self.'+element[0])
                obj.set_value(float(value))
                callback = element[1]
                if (callback != None):
                    obj.connect("value_changed",callback)

        for element in self.interface_float_adjustments:
            obj = builder.get_object(element[0])
            if obj != None:
                value = eval('self.'+element[0])
                obj.set_value(value)
                callback = element[1]
                if (callback != None):
                    obj.connect("value_changed",callback)

        for element in self.interface_lists:
            obj = eval('self.'+element[0])
            the_liststore = builder.get_object(element[0])
            the_liststore.clear()
            for item in obj:
                the_liststore.append(item)
            callback = element[1]
            if (callback != None):
                the_liststore.connect("row_changed",callback)
                the_liststore.connect("row_deleted",callback)
                the_liststore.connect("row_inserted",callback)
                the_liststore.connect("row_reordered",callback)

        for element in self.interface_colorbuttons:
            value = eval('self.'+element[0])
            obj = builder.get_object(element[0])
            objcolor = Gdk.Color(int(value[0]*65535.0),int(value[1]*65535.0),int(value[2]*65535.0))
            obj.set_color(objcolor)
            obj.set_alpha(int(value[3]*65535.0))
            callback = element[1]
            if (callback != None):
                obj.connect("color_set",callback)

        for element in self.interface_fontbuttons:
            value = eval('self.'+element[0])
            obj = builder.get_object(element[0])
            if (value != None):
                obj.set_font(value)
            callback = element[1]
            if (callback != None):
                obj.connect("font_set",callback)

        for element in self.interface_filebuttons:
            value = eval('self.'+element[0])
            obj = builder.get_object(element[0])
            if (value != None):
                obj.set_filename(value)
            callback = element[1]
            if (callback != None):
                obj.connect("file_set",callback)

        for element in self.interface_comboboxes:
            obj = eval('self.'+element[0])
            the_combo = builder.get_object(element[0])
            the_list = the_combo.get_model()
            the_list.clear()
            counter = 0
            dv = 0
            for item in element[1]:
                the_list.append([item])
                if (item == obj):
                    dv = counter
                counter += 1
            the_combo.set_active(dv)
            callback = element[2]
            if (callback != None):
                the_combo.connect("changed",callback)

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
            for element in self.interface_groups[key][0]:
                obj = builder.get_object(element)
                if obj.get_active():
                    exec('self.'+key+' = "'+element+'"')
                    break

        for element in self.interface_toggles:
            obj = builder.get_object(element[0])
            if obj.get_active():
                exec('self.'+element[0]+' = True')
            else:
                exec('self.'+element[0]+' = False')

        for element in self.interface_dualtoggles:
            obj = builder.get_object(element[0])
            if obj.get_active():
                exec('self.'+element[0]+' = True')
            else:
                exec('self.'+element[0]+' = False')

        for element in self.interface_text:
            obj = builder.get_object(element[0])
            exec('self.'+element[0]+' = obj.get_text()')

        for element in self.interface_integer_adjustments:
            obj = builder.get_object(element[0])
            if obj != None:
                exec('self.'+element[0]+' = int(obj.get_value())')

        for element in self.interface_float_adjustments:
            obj = builder.get_object(element[0])
            if obj != None:
                exec('self.'+element[0]+' = obj.get_value()')

        for element in self.interface_colorbuttons:
            obj = builder.get_object(element[0])
            objcolor = obj.get_color()
            alpha = obj.get_alpha()
            exec('self.'+element[0]+' = ((float(objcolor.red))/65535.0, (float(objcolor.green))/65535.0, (float(objcolor.blue))/65535.0, (float(alpha))/65535.0)')

        for element in self.interface_fontbuttons:
            obj = builder.get_object(element[0])
            exec('self.'+element[0]+' = obj.get_font()')

        for element in self.interface_filebuttons:
            obj = builder.get_object(element[0])
            exec('self.'+element[0]+' = obj.get_filename()')

        for element in self.interface_lists:
            exec('self.'+element[0]+' = []')
            the_liststore = builder.get_object(element[0])
            ncolumns = the_liststore.get_n_columns()
            for row in the_liststore:
                final_row = []
                for c in range(0,ncolumns):
                    final_row.append(row.model[row.iter][c])
                exec('self.'+element[0]+'.append(final_row)')

        for element in self.interface_comboboxes:
            obj = builder.get_object(element[0])
            exec('self.'+element[0]+' = element[1][obj.get_active()]')


    def save_ui(self):
        """ Makes a copy of all the UI variables """

        for element in self.interface_groups:
            exec('self.'+element+'_backup = self.'+element)
        for element in self.interface_toggles:
            exec('self.'+element[0]+'_backup = self.'+element[0])
        for element in self.interface_dualtoggles:
            exec('self.'+element[0]+'_backup = self.'+element[0])
        for element in self.interface_text:
            exec('self.'+element[0]+'_backup = self.'+element[0])
        for element in self.interface_integer_adjustments:
            exec('self.'+element[0]+'_backup = self.'+element[0])
        for element in self.interface_float_adjustments:
            exec('self.'+element[0]+'_backup = self.'+element[0])
        for element in self.interface_colorbuttons:
            exec('self.'+element[0]+'_backup = self.'+element[0])
        for element in self.interface_fontbuttons:
            exec('self.'+element[0]+'_backup = self.'+element[0])
        for element in self.interface_filebuttons:
            exec('self.'+element[0]+'_backup = self.'+element[0])
        for element in self.interface_lists:
            exec('self.'+element[0]+'_backup = self.'+element[0])
        for element in self.interface_comboboxes:
            exec('self.'+element[0]+'_backup = self.'+element[0])

    def restore_ui(self):
        """ Restores a copy of all the UI variables """

        for element in self.interface_groups:
            exec('self.'+element+' = self.'+element+'_backup')
        for element in self.interface_toggles:
            exec('self.'+element[0]+' = self.'+element[0]+'_backup')
        for element in self.interface_dualtoggles:
            exec('self.'+element[0]+' = self.'+element[0]+'_backup')
        for element in self.interface_text:
            exec('self.'+element[0]+' = self.'+element[0]+'_backup')
        for element in self.interface_integer_adjustments:
            exec('self.'+element[0]+' = self.'+element[0]+'_backup')
        for element in self.interface_float_adjustments:
            exec('self.'+element[0]+' = self.'+element[0]+'_backup')
        for element in self.interface_colorbuttons:
            exec('self.'+element[0]+' = self.'+element[0]+'_backup')
        for element in self.interface_fontbuttons:
            exec('self.'+element[0]+' = self.'+element[0]+'_backup')
        for element in self.interface_filebuttons:
            exec('self.'+element[0]+' = self.'+element[0]+'_backup')
        for element in self.interface_lists:
            exec('self.'+element[0]+' = self.'+element[0]+'_backup')
        for element in self.interface_comboboxes:
            exec('self.'+element[0]+' = self.'+element[0]+'_backup')


    def serialize(self):
        """ Returns a dictionary with both the variables of the interface and its values,
            which can be restored with unserialize
            """

        output = {}
        for element in self.interface_groups:
            output[element] = eval('self.'+element)
        for element in self.interface_toggles:
            output[element[0]] = eval('self.'+element[0])
        for element in self.interface_dualtoggles:
            output[element[0]] = eval('self.'+element[0])
        for element in self.interface_text:
            output[element[0]] = eval('self.'+element[0])
        for element in self.interface_integer_adjustments:
            output[element[0]] = eval('self.'+element[0])
        for element in self.interface_float_adjustments:
            output[element[0]] = eval('self.'+element[0])
        for element in self.interface_colorbuttons:
            output[element[0]] = eval('self.'+element[0])
        for element in self.interface_fontbuttons:
            output[element[0]] = eval('self.'+element[0])
        for element in self.interface_filebuttons:
            output[element[0]] = eval('self.'+element[0])
        for element in self.interface_lists:
            output[element[0]] = eval('self.'+element[0])
        for element in self.interface_comboboxes:
            output[element[0]] = eval('self.'+element[0])
        return output


    def unserialize(self,data_list):
        """ Takes a dictionary with the variables of the interface and its values,
            and restores them into their variables
            """

        for element in self.interface_groups:
            if element in data_list:
                exec('self.'+element+' = data_list["'+element+'"]')
        for element in self.interface_toggles:
            if element[0] in data_list:
                exec('self.'+element[0]+' = data_list["'+element[0]+'"]')
        for element in self.interface_dualtoggles:
            if element[0] in data_list:
                exec('self.'+element[0]+' = data_list["'+element[0]+'"]')
        for element in self.interface_text:
            if element[0] in data_list:
                exec('self.'+element[0]+' = data_list["'+element[0]+'"]')
        for element in self.interface_integer_adjustments:
            if element[0] in data_list:
                exec('self.'+element[0]+' = data_list["'+element[0]+'"]')
        for element in self.interface_float_adjustments:
            if element[0] in data_list:
                exec('self.'+element[0]+' = data_list["'+element[0]+'"]')
        for element in self.interface_colorbuttons:
            if element[0] in data_list:
                exec('self.'+element[0]+' = data_list["'+element[0]+'"]')
        for element in self.interface_fontbuttons:
            if element[0] in data_list:
                exec('self.'+element[0]+' = data_list["'+element[0]+'"]')
        for element in self.interface_filebuttons:
            if element[0] in data_list:
                exec('self.'+element[0]+' = data_list["'+element[0]+'"]')
        for element in self.interface_lists:
            if element[0] in data_list:
                exec('self.'+element[0]+' = data_list["'+element[0]+'"]')
        for element in self.interface_comboboxes:
            if element[0] in data_list:
                exec('self.'+element[0]+' = data_list["'+element[0]+'"]')

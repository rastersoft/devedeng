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

import cairo
from gi.repository import Gtk,Gdk,GdkPixbuf
import os
import devede.configuration_data
import devede.interface_manager

class dvd_menu(devede.interface_manager.interface_manager):

    def __init__(self,project):

        self.entry_vertical_margin = 2.0
        self.entry_separation = 2.0

        devede.interface_manager.interface_manager.__init__(self)
        self.config = devede.configuration_data.configuration.get_config()
        self.project = project

        self.default_background = os.path.join(self.config.pic_path,"backgrounds","default_bg.png")
        self.default_sound = os.path.join(self.config.pic_path,"silence.ogg")

        self.add_colorbutton("title_color", (0,0,0,1), self.update_preview)
        self.add_colorbutton("title_shadow", (0,0,0,0), self.update_preview)
        self.add_colorbutton("unselected_color", (1,1,1,1), self.update_preview)
        self.add_colorbutton("shadow_color", (0,0,0,0), self.update_preview)
        self.add_colorbutton("selected_color", (0,1,1,1), self.update_preview)
        self.add_colorbutton("background_color", (0,0,0,0.75), self.update_preview)

        self.add_text("title_text", None, self.update_preview)

        self.add_group("position_horizontal", ["left", "center", "right"], "center", self.update_preview)

        self.add_float_adjustment("margin_left", 10.0, self.update_preview)
        self.add_float_adjustment("margin_top", 12.5, self.update_preview)
        self.add_float_adjustment("margin_right", 10.0, self.update_preview)
        self.add_float_adjustment("margin_bottom", 12.5, self.update_preview)
        self.add_float_adjustment("title_horizontal", 0.0, self.update_preview)
        self.add_float_adjustment("title_vertical", 10.0, self.update_preview)

        self.add_group("at_startup", ["menu_show_at_startup", "play_first_title_at_startup"], "menu_show_at_startup")

        self.add_fontbutton("title_font", "Sans 28", self.update_preview)
        self.add_fontbutton("entry_font", "Sans 18", self.update_preview)

        self.add_filebutton("background_picture", self.default_background, self.update_preview)
        self.add_filebutton("background_music", self.default_sound, self.update_preview)

        self.cached_menu_font = None
        self.cached_menu_size = 0


    def update_preview(self,b=None):

        self.store_ui(self.builder)
        self.sf = None # force to repaint the menu
        self.wdrawing_area.queue_draw()

    def on_default_background_clicked(self,b):

        self.background_picture = self.default_background
        self.update_ui(self.builder)
        self.update_preview()

    def on_no_sound_clicked(self,b):

        self.background_music = self.default_sound
        self.update_ui(self.builder)


    def show_configuration(self):

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(self.config.gettext_domain)

        self.refresh_static_data()

        self.builder.add_from_file(os.path.join(self.config.glade,"wmenu.ui"))
        self.builder.connect_signals(self)

        self.wframe_preview = self.builder.get_object("frame_preview")
        self.wframe_preview_controls = self.builder.get_object("frame_preview_controls")
        self.wmenu = self.builder.get_object("menu")
        self.wpreview_menu = self.builder.get_object("preview_menu")
        self.wdrawing_area = self.builder.get_object("drawingarea_preview")
        self.wcurrent_page = self.builder.get_object("current_page")
        self.wshow_as_selected = self.builder.get_object("show_as_selected")
        self.wshow_as_selected.connect("toggled",self.update_preview)
        self.wmenu.show_all()

        self.pages = 0
        self.update_ui(self.builder)
        self.save_ui()


    def on_accept_clicked(self,b):

        self.wmenu.destroy()

    def on_cancel_clicked(self,b):

        self.restore_ui()
        self.wmenu.destroy()


    def on_preview_menu_clicked(self,b):
        pass


    def get_font_params(self,font_name):

        font_elements=font_name.split(" ")

        if (len(font_elements))<2:
            fontname="Sans"
            fontstyle=cairo.FONT_WEIGHT_NORMAL
            fontslant=cairo.FONT_SLANT_NORMAL
            fontsize=12
        else:
            fontname=""
            fontstyle=cairo.FONT_WEIGHT_NORMAL
            fontslant=cairo.FONT_SLANT_NORMAL
            for counter2 in range(len(font_elements)-1):
                if font_elements[counter2]=="Bold":
                    fontstyle=cairo.FONT_WEIGHT_BOLD
                elif font_elements[counter2]=="Italic":
                    fontslant=cairo.FONT_SLANT_ITALIC
                else:
                    fontname+=" "+font_elements[counter2]
            if fontname!="":
                fontname=fontname[1:]
            else:
                fontname="Sans"

        try:
            fontsize=float(font_elements[-1])
        except:
            fontsize=12

        return fontname,fontstyle,fontslant,fontsize

    def paint_arrow(self,xl,xr,y,arrow_type,left):

        if arrow_type == "menu_entry":
            fgcolor = self.unselected_color
        elif arrow_type == "menu_entry_selected":
            fgcolor = self.selected_color
        elif arrow_type == "menu_entry_activated":
            fgcolor = ( 1.0 - self.selected_color[0], 1.0 - self.selected_color[1], 1.0 - self.selected_color[2] )
        else:
            return

        fo=cairo.FontOptions()
        fo.set_antialias(cairo.ANTIALIAS_NONE)
        self.cr.set_font_options(fo)
        self.cr.set_antialias(cairo.ANTIALIAS_NONE)

        x = (xl + xr) / 2.0
        h = (self.cached_menu_size / 2.0) - 1.0
        self.cr.set_source_rgba(fgcolor[0],fgcolor[1],fgcolor[2],fgcolor[3])
        self.cr.move_to(x,y-h)
        if (left):
            self.cr.line_to(x-self.cached_menu_size+2,y)
        else:
            self.cr.line_to(x+self.cached_menu_size-2,y)
        self.cr.line_to(x,y+h)
        self.cr.line_to(x,y-h)
        self.cr.fill()

        fo=cairo.FontOptions()
        fo.set_antialias(cairo.ANTIALIAS_DEFAULT)
        self.cr.set_font_options(fo)
        self.cr.set_antialias(cairo.ANTIALIAS_DEFAULT)


    def write_text(self,text,text_type,xl,xr,y,alignment):
        """ Renders a line of text, in the rectangle delimited by xl,y-h;xr,y+h, with the specified alignment """

        if text == None:
            return

        if text_type == "title":
            fgcolor = self.title_color
            bgcolor = self.title_shadow
            hard_borders = False
            font = self.title_font
        elif text_type == "menu_entry":
            fgcolor = self.unselected_color
            bgcolor = self.shadow_color
            hard_borders = True
            font = self.entry_font
        elif text_type == "menu_entry_selected":
            fgcolor = self.selected_color
            bgcolor = None
            hard_borders = True
            font = self.entry_font
        elif text_type == "menu_entry_activated":
            fgcolor = ( 1.0 - self.selected_color[0], 1.0 - self.selected_color[1], 1.0 - self.selected_color[2] )
            bgcolor = None
            hard_borders = True
            font = self.entry_font
        else:
            return

        if hard_borders:
            fo=cairo.FontOptions()
            fo.set_antialias(cairo.ANTIALIAS_NONE)
            self.cr.set_font_options(fo)
            self.cr.set_antialias(cairo.ANTIALIAS_NONE)

        (fontname, fontstyle, fontslant, fontsize) = self.get_font_params(font)
        self.cr.select_font_face(fontname,fontslant, fontstyle)
        self.cr.set_font_size(fontsize)
        extents = self.cr.text_extents(text)

        if alignment == "left":
            x = xl
        elif alignment == "right":
            x = xr - extents[2]
        elif alignment == "center":
            x = ((xl + xr) / 2.0) - (extents[2] / 2.0)

        if (bgcolor != None):
            self.cr.move_to(x+extents[0]+2,y-(extents[3]/2.0)-extents[1]+2)
            self.cr.set_source_rgba(bgcolor[0],bgcolor[1],bgcolor[2],bgcolor[3])
            self.cr.show_text(text)

        self.cr.move_to(x+extents[0],y-(extents[3]/2.0)-extents[1])
        self.cr.set_source_rgba(fgcolor[0],fgcolor[1],fgcolor[2],fgcolor[3])
        self.cr.show_text(text)

        if hard_borders:
            fo=cairo.FontOptions()
            fo.set_antialias(cairo.ANTIALIAS_DEFAULT)
            self.cr.set_font_options(fo)
            self.cr.set_antialias(cairo.ANTIALIAS_DEFAULT)



    def refresh_static_data(self):
        """ This method sets data that can't be changed from the dvd settings window.
            It must be called before painting a menu """

        if self.config.PAL:
            self.y=576.0
        else:
            self.y=480.0

        self.title_list = []
        counter = 0
        for element in self.project.get_all_files():
            if element.show_in_menu:
                self.title_list.append( (element, counter) )
            counter += 1

        self.sf = None
        self.current_shown_page = 0


    def paint_menu(self,paint_background, paint_selected, paint_activated, page_number):

        if self.sf == None:
            self.sf=cairo.ImageSurface(cairo.FORMAT_ARGB32,720,int(self.y))
            self.cr=cairo.Context(self.sf)

        if self.cached_menu_font != self.entry_font:
            # memorize the font sizes
            (fontname, fontstyle, fontslant, fontsize) = self.get_font_params(self.entry_font)
            self.cr.select_font_face(fontname,fontslant, fontstyle)
            self.cr.set_font_size(fontsize)
            extents = self.cr.font_extents()
            self.cached_menu_size = extents[2]
            self.cached_menu_font = self.entry_font

        if paint_background:
            extra_pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.background_picture)
            extra_x = float(extra_pixbuf.get_width())
            extra_y = float(extra_pixbuf.get_height())

            self.cr.save()
            self.cr.scale(720.0/extra_x,self.y/extra_y)

            surface = Gdk.cairo_surface_create_from_pixbuf(extra_pixbuf,1,None)
            self.cr.set_source_surface(surface,0,0)
            self.cr.paint()
            self.cr.restore()
            hmargin = self.title_horizontal * 720.0 / 100.0
            self.write_text(self.title_text, "title", 0 + hmargin, 720 + hmargin, self.title_vertical * self.y / 100.0, "center")
        else:
            self.cr.set_source_rgb(1.0,1.0,1.0)
            self.cr.paint()

        top_margin_p = self.y * self.margin_top / 100.0
        bottom_margin_p = self.y * self.margin_bottom / 100.0
        left_margin_p = 720.0 * self.margin_left / 100.0
        right_margin_p = 720.0 * self.margin_right / 100.0

        entry_height = self.cached_menu_size + self.entry_vertical_margin * 2.0 + self.entry_separation
        entries_per_page = int((self.y - top_margin_p - bottom_margin_p) / entry_height)
        n_entries = len(self.title_list)
        if (n_entries > entries_per_page):
            paint_arrows = True
            entries_per_page -= 1
        else:
            paint_arrows = False

        self.pages = int(n_entries / entries_per_page)
        if (n_entries == 0) or ((n_entries % entries_per_page) != 0):
            self.pages += 1
        if (page_number >= self.pages) and (page_number > 0):
            page_number -= 1

        self.wcurrent_page.set_text(_("Page %(X)d of %(Y)d") % {"X":page_number+1 , "Y":self.pages})
        xl = left_margin_p
        xr = 720.0 - right_margin_p
        y = top_margin_p + entry_height/2.0
        for entry in self.title_list[page_number*entries_per_page:(page_number+1)*entries_per_page]:
            text = entry[0].title_name
            if paint_background:
                self.paint_base(xl, xr, y, 0)
                self.write_text(text, "menu_entry", xl, xr, y, self.position_horizontal)
            if paint_selected:
                self.write_text(text, "menu_entry_selected", xl, xr, y, self.position_horizontal)
            if paint_activated:
                self.write_text(text, "menu_entry_activated", xl, xr, y, self.position_horizontal)
            y += entry_height
        if paint_arrows:
            if page_number == 0:
                self.paint_base(xl, xr, y, 0)
                if paint_background:
                    self.paint_arrow(xl, xr, y, "menu_entry", False)
                if paint_selected:
                    self.paint_arrow(xl, xr, y, "menu_entry_selected", False)
                if paint_activated:
                    self.paint_arrow(xl, xr, y, "menu_entry_activated", False)
            elif page_number == (self.pages - 1):
                self.paint_base(xl, xr, y, 0)
                if paint_background:
                    self.paint_arrow(xl, xr, y, "menu_entry", True)
                if paint_selected:
                    self.paint_arrow(xl, xr, y, "menu_entry_selected", True)
                if paint_activated:
                    self.paint_arrow(xl, xr, y, "menu_entry_activated", True)
            else:
                self.paint_base(xl, xr, y, 1)
                self.paint_base(xl, xr, y, 2)
                med = (xl + xr) / 2.0
                if paint_background:
                    self.paint_arrow(med, xr, y, "menu_entry", False)
                    self.paint_arrow(xl, med, y, "menu_entry", True)
                if paint_selected:
                    self.paint_arrow(med, xr, y, "menu_entry_selected", False)
                    self.paint_arrow(xl, med, y, "menu_entry_selected", True)
                if paint_activated:
                    self.paint_arrow(med, xr, y, "menu_entry_activated", False)
                    self.paint_arrow(xl, med, y, "menu_entry_activated", True)

    def paint_base(self,xl, xr, y, type_b):

        height = self.cached_menu_size + self.entry_vertical_margin
        radius = (height) / 2.0
        y -= radius

        if (type_b == 1): # half button, at left
            xr = (xl+xr) / 2.0
            xr -= radius
        elif (type_b == 2): # half button, at right
            xl = (xl+xr) / 2.0
            xl += radius

        self.cr.set_source_rgba(self.background_color[0],self.background_color[1],self.background_color[2],self.background_color[3])
        self.cr.move_to(xl,y)
        self.cr.line_to(xr,y)
        self.cr.curve_to(xr+radius,y,xr+radius,y+height,xr,y+height)
        self.cr.line_to(xl,y+height)
        self.cr.curve_to(xl-radius,y+height,xl-radius,y,xl,y)
        self.cr.fill()


    def on_next_page_clicked(self,b):

        self.current_shown_page += 1
        if (self.current_shown_page == self.pages):
            self.current_shown_page -= 1
        self.update_preview()

    def on_previous_page_clicked(self,b):

        self.current_shown_page -= 1
        if (self.current_shown_page < 0):
            self.current_shown_page = 0
        self.update_preview()

    def on_drawingarea_preview_draw(self,widget,cr):

        """ Callback to repaint the menu preview window when it
            sends the EXPOSE event """

        if not self.config.menu_dynamic_preview:
            return

        if (self.sf == None):
            self.paint_menu(True, self.wshow_as_selected.get_active(), False, self.current_shown_page)
            if (self.current_shown_page >= self.pages):
                self.current_shown_page = self.pages

        cr.set_source_surface(self.sf)
        cr.paint()

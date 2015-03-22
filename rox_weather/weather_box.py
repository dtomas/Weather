# -*- coding: UTF-8 -*-
from forecast_window import ForecastWindow
from location_search_dialog import LocationSearchDialog
from rox import g, options, InfoWin, filer, OptionsBox
from urllib import urlopen, urlencode
from weather import Weather
from weather_globals import *
from xml.dom import minidom
import rox, os, gobject


class WeatherBox:

    def __init__(self, vertical = False):
        rox.setup_app_options("Weather", 'Options.xml', "rox4debian.berlios.de")
        self.o_update_interval = options.Option("update_interval", 15)
        self.o_location = options.Option("location_code", "GMXX0049 (Hamburg, Germany)")
        self.o_units = options.Option("units", "m")
        self.o_forecast_days = options.Option("forecast_days", 4)
        rox.app_options.notify()

        self.forecast_window = None

        if vertical:
            box = g.VBox()
        else:
            box = g.HBox()
        self.image = g.Image()
        self.label = g.Label("n.a.")
        
        box.pack_start(self.image)    
        box.pack_start(self.label)
        box.set_border_width(2)
        self.add(box)
        
        self.size = 0
        self.set_image('-')
        
        self.menu = g.Menu()
        
        self.weather = Weather()
        
        item = g.ImageMenuItem(g.STOCK_HELP)
        item.connect("activate", self.show_help)
        self.menu.add(item)
        
        item = g.ImageMenuItem(g.STOCK_DIALOG_INFO)
        item.connect("activate", self.show_info)
        self.menu.add(item)
        
        self.menu.append(g.SeparatorMenuItem())
        
        item = g.ImageMenuItem(_("Forecast"))
        item.get_image().set_from_file(os.path.join(rox.app_dir, 
                                                'icons', 'forecast.png'))        
        item.connect("activate", self.show_forecast)
        self.menu.append(item)

        item = g.ImageMenuItem(g.STOCK_REFRESH)
        item.connect("activate", self.update_now)
        self.menu.append(item)
        
        self.menu.append(g.SeparatorMenuItem())
        
        item = g.ImageMenuItem(g.STOCK_PREFERENCES)
        item.connect("activate", self.show_options)
        self.menu.append(item)
        
        self.menu.append(g.SeparatorMenuItem())
        
        item = g.ImageMenuItem(g.STOCK_QUIT)
        item.connect("activate", self.quit)
        self.menu.append(item)

        self.menu.show_all()
        
        self.add_events(g.gdk.BUTTON_PRESS_MASK)
        self.connect("button-press-event", self.button_pressed)
        self.connect("destroy", self.destroyed)
        
        rox.app_options.add_notify(self.options_changed)
        self.image_resizing = False
        tooltips.set_tip(self, 'n.a.')
        
        self.update_event = 0
        
        self.connect('size-allocate', self.size_allocate)
        self.connect_after('map-event', self.map_event)
        
    def get_location_code(self):
        try:
            code, name = self.o_location.value.split('(')
        except ValueError:
            return self.o_location.value # old format
        return code.strip(' ')

    def map_event(self, widget, event):
        self.update()
        time = self.o_update_interval.int_value * 60000
        self.update_event = gobject.timeout_add(time, self.update)

    def size_allocate(self, widget, rectangle):
        pass

    def resize_image(self, size):
        """Create a scaled version of the pixmap, and set image to that."""
        scaled_pixbuf = self.pixbuf.scale_simple(size, size, 
                                                g.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(scaled_pixbuf)
        self.size = size
        self.image_resizing = True 

    def destroyed(self, window):
        if self.update_event > 0:
            gobject.source_remove(self.update_event)
        
    def show_options(self, widget):
        rox.edit_options()
        
    def show_help(self, widget = None):
        filer.open_dir(os.path.join(rox.app_dir, 'Help'))
        
    def show_info(self, widget = None):
        InfoWin.infowin('Weather')
    
    def quit(self, widget):
        if rox.confirm(_("Really quit the Weather applet?"), g.STOCK_QUIT):
            self.destroy()

    def button_pressed(self, widget, event):
        if event.button == 3:
            self.menu.popup(None, None, None, event.button, event.time)
        elif event.button == 1:
            self.show_forecast(widget)
            
    def update_now(self, item = None):
        self.update()

    def update(self):
        try:
            url = ("http://xoap.weather.com/weather/local/%s?cc=*&" 
                    % self.get_location_code())
            params = { "unit" : self.o_units.value, 
                        "dayf" : 10}
            url = url + urlencode(params)
            try:
                f = urlopen(url)
            except IOError: # server or connection down 
                self.set_image('-')
                tooltips.set_tip(self, 'n.a.')
                self.label.set_text('n.a.')
                return True
            doc = minidom.parse(f)
            f.close()
            self.weather.from_xml(doc)
            tooltips.set_tip(self, str(self.weather.info))
            self.set_image(self.weather.info.icon)
            self.label.set_text("%s°%s" % (self.weather.info.temperature, 
                                                self.weather.units.temperature))
            if self.forecast_window:
                self.forecast_window.set_weather(self.weather)
        except:
            rox.report_exception()
        return True

    def show_forecast(self, widget):
        if self.forecast_window:
            self.forecast_window.destroy()
            return
        self.forecast_window = ForecastWindow(self.weather, 
                                                self.o_forecast_days.int_value)
        self.forecast_window.connect("realize", 
                                        self._forecast_window_realized)
        self.forecast_window.connect("destroy", 
                                        self._forecast_window_destroyed)
        self.forecast_window.show_all()
        self.forecast_window.present()

    def _forecast_window_destroyed(self, widget):
        self.forecast_window = None

    def _forecast_window_realized(self, widget):
        self.position_popup_window(self.forecast_window)

    def position_popup_window(self, window):
        x,y = self.window.get_origin()
        i,i, w,h, i = self.window.get_geometry()
        window.move(x,y+h)

    def set_image(self, icon_number):
        self.pixbuf = get_weather_icon(icon_number)
        if self.size < 16:
            return
        self.resize_image(self.size)
        self.image.show()

    def options_changed(self):
        if self.o_units.has_changed or self.o_location.has_changed:
            self.update()
        elif self.o_update_interval.has_changed:
            if self.update_event > 0:
                gobject.source_remove(self.update_event)
            time = self.o_update_interval.int_value * 60000
            self.update_event = gobject.timeout_add(time, self.update)
        elif self.o_forecast_days.has_changed and self.forecast_window:
            self.forecast_window.set_ndays(self.o_forecast_days.int_value)

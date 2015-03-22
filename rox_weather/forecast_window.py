# -*- coding: UTF-8 -*-
from rox import g
from weather import Weather
from weather_globals import *
import rox


class ForecastWindow(g.Window):
    
    def __init__(self, weather, ndays):
        g.Window.__init__(self, g.WINDOW_POPUP)
        self.stick()
        self.ndays = 0
        self.weather = weather
        self.table = None
        self.box = g.Frame()
        self.add(self.box)
        self.set_ndays(ndays)

    def set_ndays(self, ndays):
        self.ndays = ndays
        self.set_weather(self.weather)

    def set_weather(self, weather):
        if self.table:
            self.box.remove(self.table)
        self.table = g.Table(8, self.ndays*2)
        self.box.add(self.table)

        self.weather = weather

        self.set_title((_("Weather Forecast for ") 
                                + self.weather.info.location))

        nday = 0
        for forecast in self.weather.forecasts[:self.ndays]:

            label = g.Label()
            label.set_markup("<b>" + _(forecast.day) + "</b>")
            self.table.attach(label, nday*2, nday*2+2, 0,1)
            
            label = g.Label()
            label.set_markup("<b>" + _(forecast.date) + "</b>")
            self.table.attach(label, nday*2, nday*2+2, 1,2)
            
            label = g.Label(forecast.low + " - " 
                    + forecast.hi + " °" + self.weather.units.temperature)
            self.table.attach(label, nday*2, nday*2+2, 2,3)

            image = g.Image()
            pixbuf = get_weather_icon(forecast.day_info.icon)
            image.set_from_pixbuf(pixbuf)
            event_box = g.EventBox()
            event_box.add(image)
            tooltips.set_tip(event_box, _(forecast.day_info.description)) 
            self.table.attach(event_box, nday*2, nday*2+1, 3,4)
            
            label = g.Label(_(forecast.day_info.wind_dir))
            event_box = g.EventBox()
            event_box.add(label)
            tooltips.set_tip(event_box, _("Wind direction"))
            self.table.attach(event_box, nday*2, nday*2+1, 4,5)
            
            label = g.Label("%s %s" % (forecast.day_info.wind_speed, 
                                        self.weather.units.speed))
            event_box = g.EventBox()
            event_box.add(label)    
            tooltips.set_tip(event_box, _("Wind speed"))
            self.table.attach(event_box, nday*2, nday*2+1, 5,6)
            
            label = g.Label(forecast.day_info.humidity + "%")
            event_box = g.EventBox()
            event_box.add(label)
            tooltips.set_tip(event_box, _("Humidity"))
            self.table.attach(event_box, nday*2, nday*2+1, 6,7)
            
            label = g.Label(forecast.day_info.rain + " %")
            event_box = g.EventBox()
            event_box.add(label)
            tooltips.set_tip(event_box, _("Rain"))
            self.table.attach(event_box, nday*2, nday*2+1, 7,8)

            image = g.Image()
            pixbuf = get_weather_icon(forecast.night_info.icon)
            image.set_from_pixbuf(pixbuf)
            event_box = g.EventBox()
            event_box.add(image)
            tooltips.set_tip(event_box, _(forecast.night_info.description))
            self.table.attach(event_box, nday*2+1, nday*2+2, 3,4)

            label = g.Label(_(forecast.night_info.wind_dir))
            event_box = g.EventBox()
            event_box.add(label)
            tooltips.set_tip(event_box, _("Wind direction"))
            self.table.attach(event_box, nday*2+1, nday*2+2, 4,5)
            
            label = g.Label("%s %s" % (forecast.night_info.wind_speed, 
                                        self.weather.units.speed))
            event_box = g.EventBox()
            event_box.add(label)
            tooltips.set_tip(event_box, _("Wind speed"))
            self.table.attach(event_box, nday*2+1, nday*2+2, 5,6)
            
            label = g.Label(forecast.night_info.humidity + "%")
            event_box = g.EventBox()
            event_box.add(label)
            tooltips.set_tip(event_box, _("Humidity"))
            self.table.attach(event_box, nday*2+1, nday*2+2, 6,7)
            
            label = g.Label(forecast.night_info.rain + " %")
            event_box = g.EventBox()
            event_box.add(label)
            tooltips.set_tip(event_box, _("Rain"))
            self.table.attach(event_box, nday*2+1, nday*2+2, 7,8)

            nday += 1
        self.box.show_all()

from applet import Applet
from weather_box import WeatherBox


class WeatherApplet(Applet, WeatherBox):
    def __init__(self, xid):
        Applet.__init__(self, xid)
        WeatherBox.__init__(self, self.is_vertical_panel())
        if self.is_vertical_panel():
            self.set_size_request(8, -1)
        else:
            self.set_size_request(-1, 8)

    def size_allocate(self, widget, rectangle):
        if self.pixbuf == None:
            return
        if self.is_vertical_panel():
            size = rectangle[2]
        else:
            size = rectangle[3]
        if size != self.size:
            self.resize_image(size)

    def button_pressed(self, widget, event):
        if event.button == 3:
            self.menu.popup(None, None, 
                            self.position_menu, 
                            event.button, event.time)
        elif event.button == 1:
            self.show_forecast(widget)
from rox import Window
from weather_box import WeatherBox


class WeatherWindow(Window, WeatherBox):
    def __init__(self):
        Window.__init__(self)
        WeatherBox.__init__(self)

    def size_allocate(self, widget, rectangle):
        if self.pixbuf == None:
            return
        if self.image_resizing:
            self.image_resizing = False
            return
        size = rectangle[3]
        if size >= 16 and size != self.size:
            self.resize_image(size)

    def position_popup_window(self, window):
        x,y = self.window.get_origin()
        i,i, w,h, i = self.window.get_geometry()
        window.move(x,y+h)

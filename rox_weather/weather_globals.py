from rox import g
import rox, os

__icons = {}
tooltips = g.Tooltips()

def get_weather_icon(n):
    icon = __icons.get(n)
    if not icon:
        icon_path = os.path.join(rox.app_dir, "icons", "%s.png" % n)
        if not os.path.isfile(icon_path):
            icon_path = os.path.join(rox.app_dir, "icons", "-.png") 
        icon = g.gdk.pixbuf_new_from_file(icon_path)
        __icons[n] = icon
    return icon


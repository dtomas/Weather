from rox import OptionsBox
import gtk, gobject
from urllib import urlopen, urlencode
from xml.dom import minidom
from weather import Locations


class LocationSearchDialog(gtk.Dialog):
    # based on code from the xfce-weather-plugin
    
    def __init__(self):
        gtk.Dialog.__init__(self, _("Search weather location code"),
            flags = gtk.DIALOG_MODAL,
            buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        vbox = gtk.VBox()
        label = gtk.Label(_("Enter a city name or zip code:"))
        label.set_alignment(0, 0.5)
        vbox.pack_start(label, False)
        
        self.search_entry = gtk.Entry()
        self.search_entry.connect("activate", self.__search)
        button = gtk.Button(stock = gtk.STOCK_FIND)
        
        hbox = gtk.HBox(spacing = 2)
        hbox.pack_start(self.search_entry, False)
        hbox.pack_start(button, False)
        vbox.pack_start(hbox, False)
        
        self.result_mdl = gtk.ListStore(gobject.TYPE_STRING,
                        gobject.TYPE_STRING)
        self.result_list = gtk.TreeView(self.result_mdl)
        
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Results"), renderer, text=0)
        self.result_list.append_column(column)
        
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(self.result_list)
        
        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        frame.add(scroll)
        
        vbox.pack_start(frame, True, True)
        self.vbox.pack_start(vbox, True, True)
        vbox.set_border_width(6)
        
        button.connect("clicked", self.__search)
        self.set_size_request(350, 250)
        self.show_all()
        
    def __search(self, widget):
        search_string = self.search_entry.get_text()
        
        if not search_string:
            return False
            
        self.result_mdl.clear()
        self.result_list.set_sensitive(False)

        url = ("http://xoap.weather.com/weather/search/search?" 
                + urlencode({"where" : search_string}))
        f = urlopen(url)
        doc = minidom.parse(f)
        f.close()
        
        loc_info = Locations()
        loc_info.from_xml(doc)
        
        locations = loc_info.locations

        if locations:
            for id in locations:
                city = locations.get(id)
                it = self.result_mdl.append()
                self.result_mdl.set(it, 0, city, 1, id)
            self.result_list.set_sensitive(True)
        else:
            it = self.result_mdl.append()
            self.result_mdl.set(it, 0, _("No results"), 1, None)
        return False

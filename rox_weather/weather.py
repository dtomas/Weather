# -*- coding: UTF-8 -*-    

class Weather:
    def __init__(self):
        self.forecasts = []
        self.units = Units()
        self.info = WeatherInfoNow(self.units)
                
    def from_xml(self, doc):
        root = doc.documentElement
        for node in root.childNodes:
            if node.nodeName == 'head':
                self.units.from_xml(node)
            elif node.nodeName == 'cc':
                self.info.from_xml(node)
            elif node.nodeName == 'dayf':
                self.forecasts = []
                for child in node.childNodes:
                    if child.nodeName == 'day':
                        forecast = WeatherForecast()
                        forecast.from_xml(child)
                        self.forecasts.append(forecast)
                
class Units:
    def __init__(self):
        self.speed = ''
        self.pressure = ''
        self.distance = ''
        self.temperature = ''
        
    def from_xml(self, root):
        for node in root.childNodes:
            child_nodes = node.childNodes
            if not child_nodes:
                continue
            if node.nodeName == 'us':
                self.speed = child_nodes[0].data
            elif node.nodeName == 'ut':
                self.temperature = child_nodes[0].data
            elif node.nodeName == 'up':
                self.pressure = child_nodes[0].data
            elif node.nodeName == 'ud':
                self.distance = child_nodes[0].data

class WeatherInfo:
    def __init__(self):
        self.icon = '-'
        self.description = 'N/A'
        self.wind_speed = 'N/A'
        self.wind_dir = 'N/A'
        self.humidity = 'N/A'

    def from_xml(self, root):
        for node in root.childNodes:
            child_nodes = node.childNodes
            if not child_nodes:
                continue
            if node.nodeName == 'icon':
                self.icon = child_nodes[0].data
            elif node.nodeName == 't':
                self.description = child_nodes[0].data
            elif node.nodeName == 'hmid':
                self.humidity = child_nodes[0].data
            elif node.nodeName == 'wind':
                for child in node.childNodes:
                    child_nodes = child.childNodes
                    if not child_nodes:
                        continue
                    if child.nodeName == 's':
                        self.wind_speed = child_nodes[0].data
                    elif child.nodeName == 't':
                        self.wind_dir = child_nodes[0].data
            else:
                self.extract_node(node)

    def extract_node(self, node):
        pass
        
class WeatherInfoNow(WeatherInfo):
    def __init__(self, units):
        WeatherInfo.__init__(self)
        self.units = units
        self.location = 'N/A'
        self.time = 'N/A'
        self.temperature = 'N/A'
        self.temperature_felt = 'N/A'
        self.pressure = 'N/A'
        self.pressure_descr = 'N/A'
        self.visibility = 'N/A'
        self.uv = 'N/A'
        self.uv_descr = 'N/A'
        self.dewpoint = 'N/A'

    def extract_node(self, node):
        child_nodes = node.childNodes
        if not child_nodes:
            return
        if node.nodeName == 'lsup':
            self.time = child_nodes[0].data
        elif node.nodeName == 'obst':
            self.location = child_nodes[0].data
        elif node.nodeName == 'tmp':
            self.temperature = child_nodes[0].data
        elif node.nodeName == 'flik':
            self.temperature_felt = child_nodes[0].data
        elif node.nodeName == 'bar':
            for child in node.childNodes:
                child_nodes = child.childNodes
                if not child_nodes:
                    continue
                if child.nodeName == 'r':
                    self.pressure = child_nodes[0].data
                elif child.nodeName == 'd':
                    self.pressure_descr = child_nodes[0].data
        elif node.nodeName == 'vis':
            self.visibility = child_nodes[0].data
        elif node.nodeName == 'uv':
            for child in node.childNodes:
                child_nodes = child.childNodes
                if not child_nodes:
                    continue
                if child.nodeName == 'i':
                    self.uv = child_nodes[0].data
                elif child.nodeName == 't':
                    self.uv_descr = child_nodes[0].data
        elif node.nodeName == 'dewp':
            self.dewpoint = child_nodes[0].data
            
    def __str__(self):
        seq = ["%s: %s\n" % (_("Time"), self.time)]
        seq.append("%s: %s\n" % (_("Location"), self.location))
        seq.append("%s: %s\n" % (_("Weather"), _(self.description)))
        seq.append("%s: %s°%s" % (_("Temperature"), 
                            self.temperature, 
                            self.units.temperature))
        if self.temperature != self.temperature_felt:
            seq.append(" (%s %s°%s)" % (_("feels like"), 
                            self.temperature_felt,
                            self.units.temperature))
        seq.append("\n%s: %s %%\n" % (_("Humidity"), self.humidity))
        seq.append("%s: %s %s (%s)\n" % (_("Pressure"), self.pressure, 
                            self.units.pressure, 
                            _(self.pressure_descr)))
        seq.append("%s: %s" % (_("Wind"), _(self.wind_dir)))
        if self.wind_dir != 'CALM':
            seq.append(", %s %s" % (self.wind_speed, self.units.speed))
        seq.append("\n%s: %s %s\n" % (_("Visibility"), self.visibility, self.units.distance))
        seq.append("%s: %s (%s)\n" % (_("UV Index"), self.uv, _(self.uv_descr)))
        seq.append("%s: %s" % (_("Dew point"), self.dewpoint))
        return "".join(seq)

class WeatherInfoForecast(WeatherInfo):
    def __init__(self):
        WeatherInfo.__init__(self)
        self.rain = 'N/A'
    
    def extract_node(self, node):
        if not node.childNodes:
            return
        if node.nodeName == 'ppcp':
            self.rain = node.childNodes[0].data

class WeatherForecast:
    def __init__(self):
        self.day = "N/A"
        self.date = "N/A"
        self.hi = 'N/A'
        self.low = 'N/A'
        self.day_info = WeatherInfoForecast()
        self.night_info = WeatherInfoForecast()
        
    def from_xml(self, root):
        self.day = root.getAttribute('t')
        self.date = root.getAttribute('dt')
        for node in root.childNodes:
            child_nodes = node.childNodes
            if node.nodeName == 'hi':
                if not child_nodes:
                    continue
                self.hi = child_nodes[0].data
            elif node.nodeName == 'low':
                if not child_nodes:
                    continue
                self.low = child_nodes[0].data
            elif node.nodeName == 'part':
                day_or_night = node.getAttribute('p')
                if day_or_night == 'd':
                    self.day_info.from_xml(node)
                else:
                    self.night_info.from_xml(node)
        
class Locations:
    def __init__(self):
        self.locations = {}
        
    def from_xml(self, doc):
        for node in doc.documentElement.childNodes:
            if not node.childNodes:
                continue
            if node.nodeName == 'loc':
                id = node.getAttribute('id')
                self.locations[id] = node.childNodes[0].data

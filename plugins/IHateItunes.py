import cherrypy as cpy

class IHateItunes:
    def __init__(self, parent):
        pass

    @cpy.expose
    def index(self):
        return "<html><head><title>Hello World</title></head><body>gotcha</body></html>"

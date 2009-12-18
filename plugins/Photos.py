import cherrypy as cpy
from utils import config

class Photos(object):
    def __init__(self, parent): pass

    @cpy.expose
    def index(self):
        ns = cpy.config.get('/').copy()
        return (('head', ns), ('photo', ns), ('foot', ns))

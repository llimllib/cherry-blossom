import cherrypy as cpy
from os.path import dirname
from mako.template import Template
from mako.lookup import TemplateLookup

class PythonRuby:
    def __init__(self, parent): pass

    @cpy.expose
    def index(self):
        import pdb; pdb.set_trace()
        return TemplateLookup(directories=[dirname(__file__)]) \
                    .get_template("pyruby.mak")                \
                    .render()

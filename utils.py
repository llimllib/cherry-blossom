import cherrypy as cpy

def config(key, default=None, path='cherryblossom'):
    return cpy.config.get(key, default, path=path)

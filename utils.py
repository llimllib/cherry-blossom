import cherrypy as cpy
import time

def config(key, default=None, path='/'):
    if cpy.config.get(path):
        return cpy.config[path].get(key, default)
    return default

def run_callback(plugins, callback, *args, **kwargs):
    """
    run a callback and return all data. If the callback function returns
    a list, it will extend the return list. Tuples and dictionaries will be
    appended to the return list.
    """
    #this array just collects whatever data the plugins return and returns
    #it to the caller
    datums = []
    for p in plugins:
        if hasattr(p, callback):
            returnval = getattr(p, callback)(*args, **kwargs)
            dont_expand = [type({}), type(()), type("")]
            if returnval and type(returnval) in dont_expand:
                datums.append(returnval)
            elif returnval:
                for item in returnval:
                    datums.append(item)
    return datums

def htmlescape(text):
    """HTML excape the string"""
    return text.replace('&', '&amp;') \
               .replace('<', '&lt;') \
               .replace('>', '&gt;')

def htmlunescape(text):
    """Reverse-escapes &, <, > and " and returns a `str`."""
    return text.replace('&gt;', '>') \
               .replace('&lt;', '<') \
               .replace('&amp;', '&')

import cherrypy as cpy

def config(key, default=None, path='/'):
    if cpy.config.get(path):
        return cpy.config[path].get(key, default)
    return default

def run_callback(plugins, callback, *args, **kwargs):
    """run a callback and return all templates"""
    #this array just collects whatever data the plugins return and returns
    #it to the caller
    datums = []
    for p in plugins:
        if hasattr(p, callback):
            returnval = getattr(p, callback)(*args, **kwargs)
            if returnval and (len(returnval) == 1
                or isinstance(returnval, dict)):
                #only one item was returned, just stick it in datums
                datums.append(returnval)
            elif returnval:
                #otherwise, we need to insert each item independently
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

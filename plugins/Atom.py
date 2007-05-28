import cherrypy as cpy
import time
from cgi import escape
from urllib import basejoin as urljoin

from FileCabinet import get_most_recent, get_entries_by_meta
from utils import config

class EntryStruct(object):
    def __init__(self):
        self.desc = ''
        self.link = ''
        self.relpath = ''
        self.text = ''
        self.time = ''
        self.title = ''

class Atom(object):
    _cp_config = {"tools.etags.on" : True,
        "tools.etags.autotags" : True}

    def __init__(self, parent): pass

    @cpy.expose
    def index(self):
        cpy.tools.response_headers.headers = [('Content-Type', 'applications/xml')]
        datadir = config('datadir')
        num_entries = config('num_entries', 10)
        entries = get_most_recent(datadir, num_entries)
        return self.prepare_atom_template(entries)

    def prepare_atom_template(self, entries):
        ns = cpy.config.get('/').copy()
        entry_structs = []
        last_updated = ''
        for e in entries:
            es = EntryStruct()       
            es.title = e.title
            #If you only want short descriptions:
            #es.desc = escape(e.text[:255])
            fulltext = escape(e.text)
            es.desc = fulltext
            es.text = fulltext
            es.time = time.strftime('%Y-%m-%dT%H:%M:%SZ', e.time_tuple)
            if not last_updated: last_updated = es.time
            es.link = urljoin(config('base_url'), e.relpath + '.html')
            entry_structs.append(es)
        ns['last_updated'] = last_updated
        ns['entries'] = entry_structs
        return ('atom', ns)

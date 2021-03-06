import re, os, time
import cherrypy as cpy
from urllib import basejoin as urljoin
from FileCabinet import get_most_recent, get_entries_by_meta
from utils import config, run_callback

#regex to strip HTML
#HACK FIXME
HTML_RE = re.compile('(<.*?>)', re.DOTALL)
PARTIAL_HTML_RE = re.compile('(<[^>]$)', re.DOTALL)

class EntryStruct(object):
    def __init__(self):
        self.desc = ''
        self.link = ''
        self.relpath = ''
        self.text = ''
        self.time = ''
        self.title = ''

class Rss(object):
    #turn on etags, so we get last-modified
    _cp_config = {"tools.etags.on": True,
        "tools.etags.autotags": True,
        "tools.response_headers.on": True,
        "tools.response_headers.headers": [('Content-Type', 'application/xml')]}

    def __init__(self, parent):
        self.parent = parent

    @cpy.expose
    def index(self):
        datadir = config('datadir')
        num_entries = config('num_entries', 10)
        entries = get_most_recent(datadir, num_entries)
        return self.prepare_rss_template(entries)
    
    @cpy.expose
    def default(self, *args, **kwargs):
        if args[0].lower().startswith('keyword') and len(args) > 1:
            return self.keyword_rss(args[1])
        else: return self.index()

    def keyword_rss(self, kw):
        num_entries = config('num_entries', 10)
        entries = get_entries_by_meta('keywords')
        entries = [e for e in entries if kw in e.metadata['keywords']]
        return self.prepare_rss_template(entries[:num_entries])

    def prepare_rss_template(self, entries):
        ns = cpy.config.get('/').copy()
        entry_structs = []
        for e in entries:
            #XXX: what exactly is the <guid> element?
            #XXX: what is the category tag? should keywords go here?
            es = EntryStruct()
            es.title = e.title

            #this callback gives any interested plugins the chance to change
            #the text of a story, as presented in a feed. It gives an Entry
            #object, and ignores any return value
            run_callback(self.parent.plugins, "cb_feed_story", e)

            #because <style> messed me up, I'm going to stop stripping
            #HTML out of my description. The RSS spec sucks.
            es.desc = e.text
            es.link = urljoin(config('base_url'), e.relpath + '.html')
            es.relpath = e.relpath
            es.time = time.strftime('%Y-%m-%dT%H:%M:%SZ', e.time_tuple)
            es.text = e.text
            entry_structs.append(es)
        ns['entries'] = entry_structs
        return ('rss', ns)

    def strip_html(self, text):
        text = HTML_RE.sub('', text)
        return PARTIAL_HTML_RE.sub('', text).replace('&', '&amp;')

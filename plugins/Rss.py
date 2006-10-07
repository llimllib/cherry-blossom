import re, os, time
import cherrypy as cpy
from urllib import basejoin as urljoin
from FileCabinet import get_most_recent, get_entries_by_meta
from utils import config

#regex to strip HTML
#HACK FIXME
HTML_RE = re.compile('(<.*?>)', re.DOTALL)
PARTIAL_HTML_RE = re.compile('(<[^>]$)', re.DOTALL)

class EntryStruct:
    def __init__(self):
        self.desc = ''
        self.link = ''
        self.relpath = ''
        self.text = ''
        self.time = ''
        self.title = ''

class Rss:
    @cpy.expose
    def index(self):
        cpy.response.headerMap['Content-Type'] = "application/xml"
        #XXX: should we sanitize config file entries, or assume users are
        #      smart enough not to include (or to escape) < and > and &?
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
        cpy.response.headerMap['Content-Type'] = "application/xml"
        num_entries = config('num_entries', 10)
        entries = get_entries_by_meta('keywords')
        entries = [e for e in entries if kw in e.metadata['keywords']]
        return self.prepare_rss_template(entries[:num_entries])

    def prepare_rss_template(self, entries):
        ns = cpy.config.configMap['cherryblossom'].copy()
        entry_structs = []
        for e in entries:
            #XXX: what exactly is the <guid> element?
            #XXX: what is the category tag? should keywords go here?
            es = EntryStruct()
            es.title = e.title
            es.desc = self.strip_html(e.text)
            es.link = urljoin(config('base_url'), e.relpath)
            es.relpath = e.relpath
            es.time = time.strftime('%Y-%m-%dT%H:%M:%SZ', e.time_tuple)
            es.text = e.text
            entry_structs.append(es)
        ns['entries'] = entry_structs
        return ('rss', ns)

    def strip_html(self, text):
        text = HTML_RE.sub('', text)
        return PARTIAL_HTML_RE.sub('', text).replace('&', '&amp;')

import re
import cherrypy as cpy
from FileCabinet import get_entries_by_meta
from utils import config

#find meta info in entries
META_RE = re.compile('^<!-- ?([ \w]+): ?([\w ,.:\/-]+)-->')

#TODO: add + for keyword combination support!
class Keywords(object):
    def __init__(self, parent):
        self.keyword = ''
        self.rss_link = ''
        self.parent = parent

    @cpy.expose
    def default(self, *args, **kargs):
        if len(args) > 1:
            return self.parent.error_page("too many arguments to Keywords")
        elif len(args) < 1:
            return self.parent.error_page("Too few arguments to Keywords")
        
        self.keyword = args[0]
        
        #remember we're not sure if base_url has a trailing '/' or not...
        if 'Rss' in self.parent.plugins:
            self.rss_link = config('base_url').rstrip('/') + \
                '/Rss/keyword/' + self.keyword
        
        entries = get_entries_by_meta('keywords')
        entries = [e for e in entries if self.keyword in e.metadata['keywords']]
        return self.parent.render_page(entries)

    def cb_add_data(self):
        if self.rss_link:
            return {'keywordrss': self.rss_link, 'keyword': self.keyword}

    def cb_story(self, entry):
        """Add a $keywords variable to an entry which is a linkified,
            comma-seperated string"""
        kwstring = ''
        base_url = config('base_url')
        base_url = base_url.rstrip('/')
        #list comp for 2.3 compatibility
        kws = [k.strip() for k in entry.metadata.get('keywords', "").split(',')
                            if k != '']
        links = ['<a href=%s/Keywords/%s>%s</a>' % (base_url, kw, kw) 
                    for kw in kws]
        #add a comma seperated list of keywords to the entry
        entry.keywords = ', '.join(links)

    def cb_page_end(self):
        """clean up our data"""
        self.keyword = ''
        self.rss_link = ''

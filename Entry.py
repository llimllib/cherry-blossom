import os, time, re
import cherrypy as cpy
from utils import config
from codecs import open

#find meta info in entries
META_RE = re.compile(r'^<!-- ?([ \w]+): ?([\w ,.:\+\/-]+)-->')

#TODO: assure that all private methods/variables start with _ so that
#      they don't get included into the story's namespace
class Entry(object):
    def __init__(self, filename, datadir):
        self.filename = filename
        self.relpath, self.ext = os.path.splitext(filename.split(datadir)[-1])
        self.relpath = self.relpath.strip('\/')
        self.datefmt = config('date_fmt', '%b %d, %Y')
        self._text = u'' #will store the text of the file
        self._encoding = config('blog_encoding', 'utf-8')

        #when this is set to 1, the entry will reload from its source file
        #this can be used for a cache mechanism, but is currently unused
        self.reload_flag = 0

        self.metadata = {}
        self.parse_meta()

    def __repr__(self):
        return self.filename

    def meta(self, key, default=''):
        return self.metadata.get(key, default)

    def parse_meta(self):
        """
        parse metadata inside the text file and store it in the Entry object.
        
        metadata
        """
        #XXX: because we're storing time inside the files, we want to scan the 
        #metadata and store it in memory every time we start the server. We 
        #don't, however, want to
        #store the text of the file in memory until it is requested at least
        #once, to save on memory if there's lots of entries. Better ideas?
        #cpy.log("Parsing metadata for file %s" % self.filename)
        f = open(self.filename, encoding=self._encoding)
        #f = open(self.filename)

        #title must be the first line of the file
        self._title = f.readline().strip()
        #if 'Unicode' in self._title:
        #    import pdb; pdb.set_trace()

        #metadata lines must follow the title line immediately and begin with a 
        #hash
        for line in f:
            if not line.startswith('#'): break
            metakey, val = line[1:].strip().split(' ', 1)
            self.metadata[metakey] = val
        self.set_time()

    def set_time(self):
        """
        Set the file's time to the time specified in meta, if it exists,
        else set it to the mtime
        """
        get_mtime = True
        if self.meta('time'):
            try:
                self.time_tuple = time.strptime(self.meta('time'),
                                                config('time_fmt'))
                self.time = time.mktime(self.time_tuple)
                get_mtime = False
            except ValueError:
                #cpy.log(
                #    'file %s has an invalid time format - using mtime instead' 
                #    % self.filename)
                pass
        if get_mtime:
            self.time = os.stat(self.filename)[8]
            self.time_tuple = time.localtime(self.time)
        self.tmstr = time.strftime(self.datefmt, self.time_tuple)
    
    def gettext(self):
        '''return the file minus the first line'''
        if not self.reload_flag:
            #cpy.log('getting text of %s' % self.filename)
            txt = open(self.filename, 'r', self._encoding).readlines()
            #txt = open(self.filename).readlines()
            self.reload_flag = 1
            if len(txt) > 2:
                i = 1
                while txt[i].startswith('#'):
                    i+=1
                self._text = ''.join(txt[i:])
            else:
                self._text = ''
        return self._text

    text = property(gettext)

    def gettitle(self):
        return self._title

    title = property(gettitle)

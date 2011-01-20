#!/usr/bin/env python
import datetime, time, os, sys, traceback
import cherrypy as cpy
import FileCabinet
from utils import config, run_callback
from mako.template import Template
#print Template("hello ${data}!").render(data="world")


class BlogRoot(object):
    _cp_config = {"tools.staticdir.root": os.path.abspath(os.curdir),
                  "tools.encode.on": True,
                  "tools.encode.encoding": config("blog_encoding", "utf-8")}

    def __init__(self):
        self.timeformats =  [["%Y", "%d", "%m", "%b", "%B"],
            ["%Y %b", "%Y %m", "%Y %b", "%Y %B", "%m %d", "%b %d", "%B %d"],
            ["%Y %m %d", "%Y %b %d", "%Y %B %d"]]
        self.plugins = [] #contains all loaded plugins

        #set the output encoding
        self._cp_config["cpy.tools.encode.encoding"] = "utf-8"

        self.now = datetime.datetime.now
        self.last_update = self.now()
        self.num_entries = config('num_entries')
        self.datadir = config('datadir')
        self.ignore_directories = config('ignore_directories')
        self.fp = '' #a cache of the front page content
        self.index() #thus, we don't have to parse the metadata of the front 
                     #page article when the second request comes in
        self.init_plugins(config('plugins'))
        FileCabinet.get_most_recent(self.datadir) #initialize entries

    def render(self, templates):
        strings = []
        for t, ns in templates:
            fname = os.path.join(config('template_dir'), t + ".mak")
            print "rendering fname: %s\nwith ns: %s" % (fname, ns)
            strings.append(Template(filename=fname).render(**ns))
        return "".join(strings)

    def files(self, offset):
        return FileCabinet.get_most_recent(self.datadir, self.num_entries, \
            self.ignore_directories, offset)

    @cpy.expose
    def index(self):
        ns = cpy.config.get('/').copy()
        return self.render((('head', ns), ('index', ns), ('foot', ns)))

    @cpy.expose
    def essays(self, offset=0):
        try:
            offset = int(offset)
        except ValueError:
            offset = 0
    
        ns = cpy.config.get('/').copy()

        datadir = config('datadir')
        essays = self.files(offset)

        ns['offset'] = offset
        if len(essays) == ns['num_entries']:
            ns['offset_next'] = offset + ns['num_entries']

        ns.update({'essays': essays,
                   'offset': offset,
                   'pagename': "essays"})
        return self.render((('head', ns), ('essays', ns), ('foot', ns)))

    def init_plugins(self, pluginlist):
        """
        Initialize plugins. Assumes that each plugin contains a class of the
        same name as the file. If it does, this function attaches an instance 
        of that class to self, and adds that instance to the plugins array.
        """
        plugindir = config('plugin_dir', None)
        if not plugindir or not os.path.isdir(plugindir):
            cpy.log("Invalid Plugin Directory, no plugins loaded")
            return
        else:
            sys.path.append(plugindir)

        #XXX: Should we just scan for *.py files in the plugin dir? Should the
        # mechanism to remove a plugin be renaming it or taking it out of 
        # conf?
        for p in pluginlist:
            try:
                mod = __import__(p)
                if not hasattr(self, p):
                    instance = getattr(mod, p)(self)
                    setattr(self, p, instance)
                    self.plugins.append(instance)
                    cpy.log("successfully imported plugin module %s" % p)
                else:
                    raise ImportError
            #bare except, because the modules could raise any number of errors
            #on import, and we want them not to kill our server
            except:
                cpy.log("import failed on module %s, module not loaded" % p)
                cpy.log("%s" % sys.exc_info()[0])
                cpy.log("%s" % traceback.format_exc())

    def error_page(self, error, status=404):
        cpy.response.status = status
        ns = cpy.config.get('/')
        ns.update({'error': error})
        return self.render((('head', ns), ('error', ns), ('foot', ns)))

    def render_page(self, entries, pagename='', offset=0):
        """renders a collection of entries into a web page"""
        page = []
        #namespace for the template substitution (starts with config opts)
        ns = cpy.config.get('/').copy()

        #pagename is the page we're offsetting. see below comment.
        ns['pagename'] = pagename

        #in order to make an offset url, we need
        #$base_url/$pagename?offset=$offset&othervars=$othervars
        ns['offset'] = offset
        if len(entries) == ns['num_entries']:
            ns['offset_next'] = offset + ns['num_entries']

        #cb_add_data is the plugin's chance to add data to the story template
        #            it should return a list of dictionaries
        #XXX: really? a list of dicts? why not one dict?
        for dict_ in run_callback(self.plugins, 'cb_add_data'):
            for key, val in dict_.iteritems():
                ns[key] = val

        #let the header access the first article's info 
        if len(entries):
            for key in ('title', 'relpath', 'tmstr'):
                ns[key] = getattr(entries[0], key)
        page.append(('head', ns))

        #cb_story_start is a plugin's chance to put text between a header
        #               and all stories. Any text returned by it will be
        #               inserted there. It must return zero or more template 
        #               tuples. A template tuple consists of
        #               (template, data_dictionary) which is (string, dict)
        page.extend(run_callback(self.plugins, 'cb_story_start', entries))

        for e in entries:
            #cb_story lets a plugin insert variables just for one particular
            #         entry. It is given the story object, and may modify it.
            run_callback(self.plugins, 'cb_story', e)

            #append all story variables that do not start with "_"
            storyns = ns.copy()
            storyns.update([(key, getattr(e, key)) 
                        for key in dir(e) if not key.startswith('_')])

            page.append(('story', storyns))

        #cb_story_end is a plugin's chance to put text between all stories
        #               and the footer, similar to cb_story_start. It must
        #               return a template tuple.
        page.extend(run_callback(self.plugins, 'cb_story_end', entries))
        page.append(('foot', ns))

        #cb_page_end is a plugin's chance to clean up data
        run_callback(self.plugins, 'cb_page_end')

        return self.render(page)

    def stripall(self, str_, *strippers):
        """return a string stripped of all extensions in strippers"""
        for stripper in strippers:
            if str_.endswith(stripper):
                str_ = str_[:-len(stripper)]
        return str_

    @cpy.expose
    def default(self, *args, **kwargs):
        #allow a plugin to handle a default url if it wants; it needs to return 
        #a tuple (pagename, [Entry objects]) if it does 
        call_result = run_callback(self.plugins, 'cb_default', args) 
        if call_result != []: return self.render_page(call_result[1:], call_result[0])

        try:
            offset = int(kwargs.get('offset', 0))
        except ValueError:
            offset = 0

        z = args[0]
        l = len(args)
        if l <= len(self.timeformats):
            #check to see if args represent a date
            for fmt in self.timeformats[l-1]:
                try:
                    t = time.strptime(' '.join(args), fmt)
                    if "%Y" in fmt:
                        year = t[0]
                    else:
                        year = self.now().year
                    if "%m" in fmt or "%b" in fmt or "%B" in fmt:
                        month = t[1]
                    else:
                        month = None
                    if "%d" in fmt:
                        day = t[2]
                    else:
                        day = None
                    entries = FileCabinet.get_entries_by_date(year, month, day)
                    if entries:
                        entries = entries[offset:offset + config('num_entries')]
                        return self.render_page(entries, ' '.join(args), offset)
                except ValueError:
                    #not a date - move on
                    pass
        z = os.path.join(*args)
        fname = self.stripall(z, '.html', '.htm', '.txt')
        e = FileCabinet.get_one(fname, self.datadir)
        if e:
            return self.render_page([e])
        return self.error_page('Page Not Found', 404)

if __name__ == '__main__':
    #set our current directory to the dir with blox.py in it
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #Because I need config before instantiating BlogRoot, I need to have a
    #separate site config file; config otherwise discards everything but the
    #"global" section. Sucky.
    cpy.config.update("site.conf")
    #we need to load the config before instantiating the BlogRoot object
    cpy.config.update("cherryblossom.conf")

    cpy.quickstart(BlogRoot(), "/", "cherryblossom.conf")

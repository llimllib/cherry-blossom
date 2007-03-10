#!/usr/bin/env python
import datetime, time, os, sys, traceback
import cherrypy as cpy
import FileCabinet
from buffet import BuffetTool
from utils import config, run_callback

class BlogRoot(object):
    _cp_config = {"tools.buffet.on": True,
                  "tools.staticdir.root": os.path.abspath(os.curdir)}

    def __init__(self):
        self.months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
            'sep', 'oct', 'nov', 'dec']
        self.timeformats =  [["%Y", "%d", "%m", "%b", "%B"],
            ["%Y %b", "%Y %m", "%Y %b", "%Y %B", "%m %d", "%b %d", "%B %d"],
            ["%Y %m %d", "%Y %b %d", "%Y %B %d"]]
        self.plugins = [] #contains all loaded plugins

        #turn on the templating engine
        cpy.tools.buffet = BuffetTool(config("template_engine"),
                                      config("template_dir"))

        #and make the static root into the cd


        self.now = datetime.datetime.now
        self.last_update = self.now()
        self.num_entries = config('num_entries')
        self.datadir = config('datadir')
        self.ignore_directories = config('ignore_directories')
        self.fp = '' #a cache of the front page content
        self.index() #thus, we don't have to parse the metadata of the front 
                     #page article when the second request comes in
        self.init_plugins(config('plugins'))

    def files(self, offset):
        return FileCabinet.get_most_recent(self.datadir, self.num_entries, \
            self.ignore_directories, offset)

    @cpy.expose
    def index(self, offset=0):
        try:
            offset = int(offset)
        except ValueError:
            offset = 0
        return self.render_page(self.files(offset), offset)

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

    def error_page(self, error):
        ns = cpy.config.get('/')
        ns.update({'error': error})
        return (('head', ns), ('error', ns), ('foot', ns))

    def render_page(self, entries, offset=0):
        """renders a collection of entries into a web page"""
        page = []
        #namespace for the template substitution (starts with config opts)
        ns = cpy.config.get('/')

        #in order to make an offset url, we need
        #$base_url/$currentModule(s)?offset=$offset&othervars=$othervars
        if len(entries) == ns['num_entries']:
            ns['offset'] = offset + ns['num_entries']

        #cb_add_data is the plugin's chance to add data to the story template
        #            it should return a list of
        for dict_ in run_callback(self.plugins, 'cb_add_data'):
            for key, val in dict_.iteritems():
                ns[key] = val

        #let the header access the first article's info 
        if len(entries):
            for key in ('title', 'text', 'relpath', 'tmstr'):
                ns[key] = getattr(entries[0], key)

        page.append(('head', ns))

        #cb_story_start is a plugin's chance to put text between a header
        #               and all stories. Any text returned by it will be
        #               inserted there. It must return one or more template 
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

        return page

    def stripall(self, str, *strippers):
        """return a string stripped of all extensions in strippers"""
        for stripper in strippers:
            if str.endswith(stripper):
                str = str[:-len(stripper)]
        return str

    @cpy.expose
    def default(self, *args):
        #allow a plugin to handle a default url if it wants; it needs to return 
        #Entry objects if it does 
        files = run_callback('cb_default', args) 
        if files != []: return self.render_page(files)

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
                        return self.render_page(entries)
                except ValueError:
                    #not a date - move on
                    pass
        z = os.path.join(*args)
        fname = self.stripall(z, '.html', '.htm', '.txt')
        e = FileCabinet.get_one(fname, self.datadir)
        if e:
            return self.render_page([e])
        return self.error_page('Page Not Found')

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

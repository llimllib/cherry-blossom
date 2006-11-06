#!/usr/bin/env python
import datetime, time, os, sys, traceback
import cherrypy as cpy
import FileCabinet
from buffet import TemplateFilter
from utils import config

#TODO: make installer automatically download prereqs - does this happen by
#       default with easy_install?
#TODO: improve caching. Not sure how though. Ideas?
#TODO: Admin module - add entries, invalidate cache, allow plugins a callback
#                       to put info here.
#TODO: Documentation. I'm not gonna do it. Anyone game?
#TODO: Config - Required config elements should be verified at startup (slashes
#       or no slashes, email must be present & valid, etc)
#QUESTION: Should the program use the cherrypy filter system instead of its
#          own? Does this program not fit the "zen of cherrypy"?
class BlogRoot(object):
    #TODO: parameterize this (I can't get server.output.filters to work, and
    #                           we can't reference config here (?))
    _cp_filters = [
        #set type of template and location of template directory
        TemplateFilter('cheetah', 'templates')]

    def __init__(self):
        cpy.config.update(file="cherryblossom.conf")  

        self.timeformats =  [["%Y", "%d", "%m", "%b", "%B"],
            ["%Y %b", "%Y %m", "%Y %b", "%Y %B", "%m %d", "%b %d", "%B %d"],
            ["%Y %m %d", "%Y %b %d", "%Y %B %d"]]
        self.plugins = [] #contains all loaded plugins

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
                    instance = getattr(mod, p)()
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

    def run_callback(self, callback, *args, **kwargs):
        """run a callback and return all templates"""
        #this array just collects whatever data the plugins return and returns
        #it to the caller
        datums = []
        for p in self.plugins:
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

    def error_page(self, error):
        ns = cpy.config.configMap['cherryblossom']
        ns.update({'error': error})
        return (('head', ns), ('error', ns), ('foot', ns))

    def render_page(self, entries, offset=0):
        """renders a collection of entries into a web page"""
        page = []
        #namespace for the template substitution (starts with config opts)
        ns = cpy.config.configMap['cherryblossom'].copy()

        #in order to make an offset url, we need
        #$base_url/$currentModule(s)?offset=$offset&othervars=$othervars
        if len(entries) == ns['num_entries']:
            ns['offset'] = offset + ns['num_entries']

        #cb_add_data is the plugin's chance to add data to the story template
        #            it should return a list of
        for dict_ in self.run_callback('cb_add_data'):
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
        page.extend(self.run_callback('cb_story_start', entries))

        for e in entries:
            #cb_story lets a plugin insert variables just for one particular
            #         entry. It is given the story object, and may modify it.
            self.run_callback('cb_story', e)

            #append all story variables that do not start with "_"
            storyns = ns.copy()
            storyns.update([(key, getattr(e, key)) 
                        for key in dir(e) if not key.startswith('_')])

            page.append(('story', storyns))

        #cb_story_end is a plugin's chance to put text between all stories
        #               and the footer, similar to cb_story_start. It must
        #               return a template tuple.
        page.extend(self.run_callback('cb_story_end', entries))
        page.append(('foot', ns))

        #cb_page_end is a plugin's chance to clean up data
        self.run_callback('cb_page_end')

        return page

    def stripall(self, str, *strippers):
        """return a string stripped of all extensions in strippers"""
        for stripper in strippers:
            if str.endswith(stripper):
                str = str[:-len(stripper)]
        return str

    @cpy.expose
    def default(self, *args):
        z = args[0]
        l = len(args)
        if l < len(self.timeformats):
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

    cpy.root = BlogRoot()
    cpy.server.start()

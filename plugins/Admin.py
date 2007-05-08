import cherrypy as cpy
import md5
import os
import FileCabinet
from utils import config, htmlescape, htmlunescape, run_callback

class Admin(object):
    _cp_config = {"tools.basic_auth.on": True,
        "tools.basic_auth.realm": "localhost",
        "tools.basic_auth.users": {config("admin_user"): 
                                   md5.new(config("admin_pw")).hexdigest()},
        "tools.expires.on": True}

    def __init__(self, parent):
        self.parent = parent

    @cpy.expose
    def index(self):
        #TODO: what's the right redirect to give here?
        raise cpy.InternalRedirect("/Admin/ls")

    def navbar(self, ns):
        """Run a callback so that any module can add an element to the Admin
        navbar"""
        ns['modules'] = run_callback(self.parent.plugins, "cb_admin_navbar", )
        return ('admin_head', ns)

    def cb_admin_navbar(self):
        return {'link': 'ls', 'title': 'Edit Stories'}

    @cpy.expose
    def edit(self, filename):
        try:
            #XXX: are we sure that filename can't ref previous dirs? ../ didn't
            #       work in my basic test, but how should we better sanitize this?
            fullname = os.path.join(config("datadir"), filename)
            f = file(fullname)
        except IOError:
            cpy.log("Unable to open file %s for editing" % fullname)
            return
        title = "Editing file %s" % filename
        story_title = f.readline()
        body = htmlescape(f.read())

        ns = locals()
        del ns['self']

        return [self.navbar(ns), ('admin_storyedit', ns)]

    @cpy.expose
    def update_story(self, story_title="", story_body="", filename=""):
        if story_title == "" or story_body == "" or filename == "":
            raise cpy.InternalRedirect("ls")

        filename = os.path.join(config('datadir'), filename)
        tmpfile = filename + ".bak"
        try:
            f = open(tmpfile, 'w')
            f.write(story_title + "\n")
            f.write(htmlunescape(story_body))
        except Exception, e:
            os.unlink(tmpfile)
            cpy.log("unable to log: " + e.Message)
        finally:
            f.close()
        os.rename(tmpfile, filename)

        return [self.navbar({"title": "Successfully updated"}),
                ('admin_updated', {"filename": f})]

    @cpy.expose
    def ls(self, dir=""):
        dirname = os.path.join(config('datadir'), dir)
        l = [f for f in os.listdir(dirname) if f.endswith('.txt')]
        title = "Listing dir %s" % dir

        ns = locals()
        del ns['self']

        return [self.navbar(ns), ('admin_ls', ns)]

    @cpy.expose
    def default(self, *args, **kwargs):
        try:
            f = args[0]
        except ValueError: pass

        #cb_admin_call should return (("template1", {namespace}), ("template2", {ns})) 
        #if it handles function f
        page = [self.navbar({'title': f})]
        page.extend(run_callback(self.parent.plugins, "cb_admin_call", f))
        print page
        return page

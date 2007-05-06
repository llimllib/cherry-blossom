import cherrypy as cpy
import md5
import os
import FileCabinet
from utils import config, htmlescape, htmlunescape

class Admin(object):
    _cp_config = {"tools.basic_auth.on": True,
        "tools.basic_auth.realm": "localhost",
        "tools.basic_auth.users": {config("admin_user"): 
                                   md5.new(config("admin_pw")).hexdigest()},
        "tools.expires.on": True}

    def __init__(self, parent): pass

    @cpy.expose
    def index(self):
        #TODO: what's the right redirect to give here?
        raise cpy.InternalRedirect("/Admin/ls")

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

        return [('admin_head', ns), ('admin_storyedit', ns)]

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
            import pdb; pdb.set_trace()
            os.unlink(tmpfile)
            cpy.log("unable to log: " + e.Message)
        finally:
            f.close()
        os.rename(tmpfile, filename)

        return [('admin_head', {"title": "Successfully updated"}),
                ('admin_updated', {"filename": f})]

    @cpy.expose
    def ls(self, dir=""):
        dirname = os.path.join(config('datadir'), dir)
        l = [f for f in os.listdir(dirname) if f.endswith('.txt')]
        title = "Listing dir %s" % dir

        ns = locals()
        del ns['self']

        return [('admin_head', ns), ('admin_ls', ns)]

"""
CONFIGURATION PARAMETERS:

commentdir (string): Directory in which to keep/find comments
"""

import re, os, time
import cherrypy as cpy
from urllib import basejoin as urljoin
from utils import config

class CommentStruct(object):
    def __init__(self):
        self.text = ''
        self.url = ''
        self.author = ''
        self.email = ''
        self.filename = ''
        self.story = ''

class CommentError(Exception):
    pass

class Comments(object):
    def __init__(self, parent):
        commentdir = config('commentdir', None, 'comments')
        if not commentdir:
            raise CommentError, "Commentdir not found in config file"

        if os.path.isdir(commentdir):
            self.commentdir = commentdir
        else:
            raise CommentError, "Comment Directory Not Found"

        self.sanitize = re.compile('\W').sub

    def delete(self, filename):
        try:
            os.unlink(os.path.join(self.commentdir, filename))
        except OSError:
            cpy.log("unable to delete file %s" % filename)

    @cpy.expose
    def add(self, story='', author='', email='', url='', comment='', **kwargs):
        if not (comment and story):
            return "invalid comment form"
        s_story = self.sanitize('_', story) #s_ for sanitized
        fname = os.path.join(self.commentdir, s_story + '.' + str(time.time()))
        while os.path.isfile(fname):
            fname = s_story + '.' + str(time.time())
        f = file(fname, 'w')
        #Assumes no \n inside name and email
        f.write(story + '\n')
        f.write(author.strip() + '\n')
        f.write(email.strip() + '\n')
        f.write(url.strip() + '\n')
        f.write(comment)
        f.close()
        redirect = config('base_url') + story
        cpy.log('redirecting to %s' % redirect)

        raise cpy.HTTPRedirect(redirect)

    def count_comments(self, story):
        #TODO: this won't work for some fnames: i.e. /deep/deep.txt and 
        #     _deep_deep.txt will share comments. How to fix? Q: What is always
        #    unique about an entry?
        n = 0
        for f in os.listdir(self.commentdir):
            if f.startswith(self.sanitize('_', story)):
                n += 1
        return n

    def get_comments(self, story):
        """given a story's relpath, return the comment template for that 
            story"""
        comments = []
        for f in os.listdir(self.commentdir):
            fin = file(os.path.join(self.commentdir, f))
            fstory = fin.readline().strip()
            if fstory == story:
                lines = fin.readlines()

                cmt = CommentStruct()
                cmt.filename = f
                cmt.story = fstory
                cmt.author, cmt.email, cmt.url = [l.strip() for l in lines[:3]]
                cmt.text = ''.join(lines[3:])
                comments.append(cmt)
        return ('comments', {'comments': comments})

    def get_all_comments(self):
        """return all comments, regardless of story"""
        comments = []
        for f in os.listdir(self.commentdir):
            fin = file(os.path.join(self.commentdir, f))
            fstory = fin.readline().strip()
            lines = fin.readlines()

            cmt = CommentStruct()
            cmt.filename = f
            cmt.story = fstory
            cmt.author, cmt.email, cmt.url = [l.strip() for l in lines[:3]]
            cmt.text = ''.join(lines[3:])
            comments.append(cmt)
        return comments

    def cb_story(self, entry):
        """Add the number of comments to the entry's namespace"""
        #XXX: is it right to modify the actual entry object permanently with
        #     this? It sticks in my craw a bit
        entry.n_comments = self.count_comments(entry.relpath)
        #mako doesn't allow us to modify or create variables outside of a
        #dictionary, so give it one.
        entry.attributes = {}

    def cb_story_end(self, entries):
        """If this is a single entry, get the comments and add the 
        "Add Comment" form"""
        if len(entries) == 1:
            story = entries[0].relpath
            return [self.get_comments(story), self.comment_form(story)]

    def comment_form(self, story):
        url = urljoin(config('base_url'), '/Comments/add')
        return ('comment_form', {'url': url, 'story':story})

    def cb_admin_navbar(self):
        return [('ls_comments', 'List Comments')]

    def cb_admin_call(self, f, args, kwargs):
        if f == "ls_comments":
            return ('admin_ls_comments', {'comments': self.get_all_comments()})
        if f == "delete_comments":
            deletes = kwargs['delete_filename']
            if len(deletes) == 0: return
            elif type(deletes) == type(''): deletes = [deletes]

            import pdb; pdb.set_trace()
            for f in deletes:
                self.delete(f)

            raise cpy.HTTPRedirect("/Admin/ls_comments")

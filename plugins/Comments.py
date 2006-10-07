import re, os, time
import cherrypy as cpy
from urllib import basejoin as urljoin
from utils import config

"""
CONFIGURATION PARAMETERS:

commentdir (string): Directory in which to keep/find comments
"""

class CommentStruct:
    def __init__(self):
        self.text = ''
        self.url = ''
        self.author = ''
        self.email = ''

class CommentError(Exception):
    pass

class Comments:
    def __init__(self):
        commentdir = config('commentdir', None, 'comments')
        if not commentdir:
            raise CommentError, "Commentdir not found in config file"

        if os.path.isdir(commentdir):
            self.commentdir = commentdir
        else:
            raise CommentError, "Comment Directory Not Found"

        self.sanitize = re.compile('\W').sub

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
            f = file(os.path.join(self.commentdir, f))
            fstory = f.readline().strip()
            if fstory == story:
                cmt = CommentStruct()
                lines = f.readlines()
                cmt.author, cmt.email, cmt.url = [l.strip() for l in lines[:3]]
                cmt.text = ''.join(lines[3:])
                comments.append(cmt)
        return ('comments', {'comments': comments})

    def cb_story(self, entry):
        """Add the number of comments to the entry's namespace"""
        #XXX: is it right to modify the actual entry object permanently with
        #     this? It sticks in my craw a bit
        entry.n_comments = self.count_comments(entry.relpath)

    def cb_story_end(self, entries):
        """If this is a single entry, get the comments and add the 
        "Add Comment" form"""
        if len(entries) == 1:
            story = entries[0].relpath
            return (self.get_comments(story), self.comment_form(story))

    def comment_form(self, story):
        url = urljoin(config('base_url'), '/Comments/add')
        return ('comment_form', {'url': url, 'story':story})

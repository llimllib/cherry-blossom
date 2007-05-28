"""Prerequisites: pygments (http://pygments.org)

Configuration for SyntaxHighlight module should be in a [SyntaxHighlight] 
    secion of your cherryblossom.conf file.

options:
syntax_style (string): Style to use for highlighting text. Check out the style 
    documentation at http://pygments.org/docs/styles/ and take the styles out 
    for a test drive at http://pygments.org/demo/"""

import cherrypy as cpy
import re
import pygments
from cgi import escape
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from utils import config

CODE_RE = re.compile("<code (?:\s*lang=(.*?))*>(.*?)<(?#)/code>", re.S)

class SyntaxHighlight(object):
    def __init__(self, parent):
        #so that if cb_feed_render_story gets called before _story_start,
        #we don't throw an error
        self.render_css = True

    def cb_story_start(self, entries):
        self.render_css = True

    def highlight_code(self, textstr):
        for lang, code in CODE_RE.findall(textstr):
            if not lang: lang = "python"

            try:
                lexer = get_lexer_by_name(lang.strip('"'))
            except ClassNotFound:
                return
            formatter = HtmlFormatter(style=config("syntax_style", "default", 
                "SyntaxHighlight"))
            code = pygments.highlight(code, lexer, formatter)

            if self.render_css:
                code = '<style type="text/css">%s</style>\n%s' % \
                    (formatter.get_style_defs(), code)
                self.render_css = False
            textstr = CODE_RE.sub(code, textstr, 1)
        return textstr

    #story is an Entry
    def cb_feed_story(self, story):
        #de-lazify the object
        story.text
        story._text = self.highlight_code(story._text)
        
    #story is an Entry object
    def cb_story(self, story):
        #de-lazify the object
        story.text
        story._text = self.highlight_code(story._text)

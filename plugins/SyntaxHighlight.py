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
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from utils import config

CODE_RE = re.compile("<code (?:\s*lang=(.*?))*>(.*?)<(?#)/code>", re.S)

class SyntaxHighlight(object):
    def __init__(self, parent): pass

    def cb_story_start(self, entries):
        self.render_css = True

    #story is an Entry object
    def cb_story(self, story):
        for lang, code in CODE_RE.findall(story._text):
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
            story._text = CODE_RE.sub(code, story._text, 1)

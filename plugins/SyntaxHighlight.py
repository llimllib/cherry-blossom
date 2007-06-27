"""Prerequisites: pygments (http://pygments.org)

To get code highlighting, you'll need to generate a CSS file from your
favorite Pygments theme and include it in your header; see an example css
file at http://billmill.org:9561/cherry_blossom/browser/trunk/static/code.css
. If you want to generate the CSS on the fly, check out this earlier revision
of SyntaxHighlighter which did so:
http://billmill.org:9561/cherry_blossom/browser/trunk/plugins/SyntaxHighlight.py?rev=197


Configuration for SyntaxHighlight module should be in a [SyntaxHighlight] 
    secion of your cherryblossom.conf file.

options:
syntax_style (string): Style to use for highlighting text. Check out the style 
    documentation at http://pygments.org/docs/styles/ and take the styles out 
    for a test drive at http://pygments.org/demo/
"""

import cherrypy as cpy
import re
import pygments
from cgi import escape
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from utils import config

CODE_RE = re.compile("<code (?:\s*lang=(.*?))*>(.*?)<(?#)/code>", re.S)

class SyntaxHighlight(object):
    def __init__(self, parent): pass

    def highlight_code(self, textstr, font_tags=False):
        for lang, code in CODE_RE.findall(textstr):
            if not lang: lang = "python"

            try:
                lexer = get_lexer_by_name(lang.strip('"'))
            except ClassNotFound:
                return
            formatter = HtmlFormatter(style=config("syntax_style", "default", 
                "SyntaxHighlight"), noclasses=font_tags)
            code = pygments.highlight(code, lexer, formatter)

            textstr = CODE_RE.sub(code, textstr, 1)
        return textstr

    #story is an Entry object
    def cb_feed_story(self, story):
        #de-lazify the object
        story.text
        story._text = self.highlight_code(story._text, font_tags=True)
        
    #story is an Entry object
    def cb_story(self, story):
        #de-lazify the object
        story.text
        story._text = self.highlight_code(story._text)

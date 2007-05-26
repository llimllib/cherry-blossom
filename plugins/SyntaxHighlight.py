import cherrypy as cpy
import re
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

CODE_RE = re.compile("<code (?:\s*lang=(.*?))*>(.*?)<(?#)/code>", re.S)

class SyntaxHighlight(object):
    def __init__(self, parent): pass

    def cb_story_start(self, entries):
        self.render_css = True

    #story is an Entry
    def cb_story(self, story):
        for lang, code in CODE_RE.findall(story._text):
            if not lang: lang = "python"

            lexer = get_lexer_by_name(lang)
            formatter = HtmlFormatter(style='trac')
            code = pygments.highlight(code, lexer, formatter)

            if self.render_css:
                code = '<style type="text/css">%s</style>\n%s' % \
                    (formatter.get_style_defs(), code)
                story._text = CODE_RE.sub(story._text, code, 1)
                self.render_css = False
            else:
                story._text = CODE_RE.sub(story._text, code, 1)

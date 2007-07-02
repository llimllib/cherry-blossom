import sys
from urllib import urlopen
from cStringIO import StringIO

import twill

import cherrypy as cpy
sys.path.insert(0, "..")
import blox

def setup():
    cpy.config.update("site.conf")
    cpy.config.update("basic.conf")
    wsgi = cpy.tree.mount(blox.BlogRoot(), "/", "basic.conf")
    wsgi = cpy.tree.mount(blox.BlogRoot(), "/", "basic.conf")
    twill.add_wsgi_intercept('localhost', 4444, lambda: wsgi)
    syserr, sys.stderr = sys.stderr, StringIO()
    try:
        cpy.engine.start(blocking=False)
    finally:
        sys.stderr = syserr

def testIndex():
    test = """
    extend_with header
    debug commands 1

    go /
    code 200
    header charset=utf-8
    """
    twill.execute_string(test, initial_url='http://localhost:4444')

def testi18n():
    test = """
    debug commands 1

    go /test_i18n.html
    code 200
    find 'I\xc3\xb1t\xc3\xabrn\xc3\xa2ti\xc3\xb4n\xc3\xa0liz\xc3\xa6ti\xc3\xb8n'
    """
    twill.execute_string(test, initial_url='http://localhost:4444')
    browser = twill.get_browser()
    print dir(browser)

def teardown(module):
    twill.remove_wsgi_intercept('localhost', 4444)
    cpy.engine.stop()

if __name__ == "__main__":
    #start the server so I can see what it looks like
    cpy.config.update("site.conf")
    cpy.config.update("basic.conf")
    cpy.quickstart(blox.BlogRoot(), "/", "basic.conf")

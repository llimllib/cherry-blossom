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
    twill.add_wsgi_intercept('localhost', 4444, lambda: wsgi)
    syserr, sys.stderr = sys.stderr, StringIO()
    try:
        cpy.engine.start(blocking=False)
    finally:
        sys.stderr = syserr

def testIndex():
    test = """
    debug commands 1

    go /
    code 200
    """
    twill.execute_string(test, initial_url='http://localhost:4444')

def teardown(module):
    twill.remove_wsgi_intercept('localhost', 4444)
    cpy.engine.stop()

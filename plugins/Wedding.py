"""
Configuration for comments module should be in a [comments] secion of your
    cherryblossom.conf file.

options:
commentdir (string): Directory in which to keep/find comments
"""

import re, os, time
import cherrypy as cpy
from urllib import basejoin as urljoin
from utils import config

class Wedding(object):
    def __init__(self, parent): self.parent = parent

    @cpy.expose
    def default(self, *args, **kwargs):
        raise cpy.HTTPRedirect("http://billmill.org/wedding/")

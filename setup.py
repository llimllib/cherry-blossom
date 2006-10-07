#!/usr/bin/env python
import glob, os
from setuptools import setup, find_packages

template_list = glob.glob(os.path.join('templates', '*.tmpl'))

setup(name='cherry_blossom', 
        version='1.0', 
        description='A blog server like pybloxsom, but written in cherrypy',
        author='Bill Mill',
        author_email='bill.mill@gmail.com',
        url='billmill.org',
        py_modules=['Entry', 'FileCabinet', 'blox'],
        packages=['plugins'],
        include_package_data = True,
        license="Public Domain",
      )

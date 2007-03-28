#!/usr/bin/env python


"""
Autogenerated by CHEETAH: The Python-Powered Template Engine
 CHEETAH VERSION: 1.0
 Generation time: Tue Mar 27 22:57:42 2007
   Source file: head.tmpl
   Source file last modified: Sun Mar 11 12:29:39 2007
"""

__CHEETAH_genTime__ = 'Tue Mar 27 22:57:42 2007'
__CHEETAH_src__ = 'head.tmpl'
__CHEETAH_version__ = '1.0'

##################################################
## DEPENDENCIES

import sys
import os
import os.path
from os.path import getmtime, exists
import time
import types
import __builtin__
from Cheetah.Template import Template
from Cheetah.DummyTransaction import DummyTransaction
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers

##################################################
## MODULE CONSTANTS

try:
    True, False
except NameError:
    True, False = (1==1), (1==0)
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time

##################################################
## CLASSES

class head(Template):
    """
    
    Autogenerated by CHEETAH: The Python-Powered Template Engine
    """

    ##################################################
    ## GENERATED METHODS


    def __init__(self, *args, **KWs):
        """
        
        """

        Template.__init__(self, *args, **KWs)

    def respond(self,
            trans=None,
            VFFSL=valueFromFrameOrSearchList,
            VFN=valueForName):


        """
        This is the main method generated by Cheetah
        """

        if not trans: trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            dummyTrans = True
        else: dummyTrans = False
        write = trans.response().write
        SL = self._searchList
        globalSetVars = self._globalSetVars
        filter = self._currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <link rel="shortcut icon" href="static/favicon.ico" type="image/x-icon">
    <link rel="icon" href="static/favicon.ico" type="image/x-icon">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>''')
        __v = VFFSL(SL,"getVar",False)('blog_title', '')
        if __v is not None: write(filter(__v, rawExpr="$getVar('blog_title', '')")) # from line 7, col 8.
        write(' \r\n')
        if VFFSL(SL,"varExists",False)('title'):
            write('    - ')
            __v = VFFSL(SL,"getVar",False)('title', '')
            if __v is not None: write(filter(__v, rawExpr="$getVar('title', '')")) # from line 9, col 7.
            write('\r\n')
        write('''</title>
<link href="/static/styles.css" rel="stylesheet" type="text/css" />
<style type="text/css">
</style>
</head>
<body>

<div id="box"><!-- Begin Container Box -->
<!--<div id="header"></div>-->
<div id="main"><!-- Begin Main Content -->

''')
        if VFFSL(SL,"varExists",False)('keywordrss'):
            write('  <a href="')
            __v = VFFSL(SL,"keywordrss",True)
            if __v is not None: write(filter(__v, rawExpr='$keywordrss')) # from line 23, col 12.
            write('">Rss for keyword</a>\r\n')
        
        ########################################
        ## END - generated method body
        
        return dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## GENERATED ATTRIBUTES


    __str__ = respond

    _mainCheetahMethod_for_head= 'respond'


# CHEETAH was developed by Tavis Rudd, Mike Orr, Ian Bicking and Chuck Esterbrook;
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org

##################################################
## if run from command line:
if __name__ == '__main__':
    head().runAsMainProgram()


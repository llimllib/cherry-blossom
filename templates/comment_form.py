#!/usr/bin/env python


"""
Autogenerated by CHEETAH: The Python-Powered Template Engine
 CHEETAH VERSION: 1.0
 Generation time: Tue Mar 27 22:57:42 2007
   Source file: comment_form.tmpl
   Source file last modified: Sat Jan 20 01:06:17 2007
"""

__CHEETAH_genTime__ = 'Tue Mar 27 22:57:42 2007'
__CHEETAH_src__ = 'comment_form.tmpl'
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

class comment_form(Template):
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
        
        write('<form method="post" action="')
        __v = VFFSL(SL,"url",True)
        if __v is not None: write(filter(__v, rawExpr='$url')) # from line 1, col 29.
        write('" name="comments_form">\r\n<input type="hidden" name="secretToken" value="pleaseDontSpam" />\r\n<input name="story" type="hidden" value="')
        __v = VFFSL(SL,"story",True)
        if __v is not None: write(filter(__v, rawExpr='$story')) # from line 3, col 42.
        write('''" />
Name:<br />
<input maxlength="50" name="author" size="50" type="text" value="" />
<br /><br />
E-mail:<br />
<input maxlength="75" name="email" size="50" type="text" value="" />
<br /><br />
URL:<br />
<input maxlength="100" name="url" size="50" type="text" value="" />
<br /><br />
Comment:<br />
<textarea cols="50" name="comment" rows="12"></textarea>
<br /><br />
<input name="Submit" type="submit" value="Submit" />
</form>
''')
        
        ########################################
        ## END - generated method body
        
        return dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## GENERATED ATTRIBUTES


    __str__ = respond

    _mainCheetahMethod_for_comment_form= 'respond'


# CHEETAH was developed by Tavis Rudd, Mike Orr, Ian Bicking and Chuck Esterbrook;
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org

##################################################
## if run from command line:
if __name__ == '__main__':
    comment_form().runAsMainProgram()


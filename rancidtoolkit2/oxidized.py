#!/usr/bin/env python
#
# Written by Marcus Stoegbauer <ms@man-da.de>

"""
"""
import sys
import re
import os.path
from rtconfig import rtconfig

class oxidized(rtconfig):

    def __init__(self, oxidized_url=""):
        if type(oxidized_url) != str or oxidized_url == "":
            if sys.platform == "darwin":
                oxidized_url = "http://dazzle.office.man-da.de:8888"
        super(oxidized, self).__init__(method="oxidized", oxidized_url=oxidized_url);
    # __init

    def getActiveDevices(self):
        pass
    # getActiveDevices

    def getRouter(self, device):
        pass
    # getRouter

    def getConfig(self, device):
        pass
    # getConfig
# class oxidized
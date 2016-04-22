#!/usr/bin/env python
#
# Written by Marcus Stoegbauer <ms@man-da.de>

"""
"""
import sys
import re
import os.path
from rtconfig import rtconfig

class rancid(rtconfig):

    __locations = list()
    __rancid_base = ""

    def __init__(self, locations=None, rancid_base=""):
        if locations is None and rancid_base == "":
            if sys.platform == "darwin":
                locations = ["darmstadt", "frankfurt", "wiesbaden",
                             "amsterdam", "momus", "test", "hmwk",
                             "tiz"]
                rancid_base = "/Users/lysis/share/rancid"
            else:
                locations = ["darmstadt", "frankfurt", "wiesbaden",
                             "amsterdam", "momus", "tiz"]
                rancid_base = "/home/rancid/var"
        else:
            if type(locations) == str:
                locations = [locations]
            if type(locations) != list:
                raise TypeError("locations is not list or string")
            # if locations

            if type(rancid_base) != str:
                raise TypeError("rancid_base is not string")
        # if empty
        super(rancid, self).__init__(method="rancid", locations=locations, rancid_base=rancid_base);    
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

# class rancid

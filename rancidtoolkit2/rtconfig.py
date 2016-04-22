#!/usr/bin/env python
#
# Written by Marcus Stoegbauer <ms@man-da.de>

"""
"""
import sys
import re
import os.path

class rtconfig(object):

    __method = ""
    __base_url = ""
    __locations = list()
    __rancid_base = ""

    def __init__(self, method="", locations=None, rancid_base="", oxidized_url=""):
        if method == "" and oxidized_url != "":
            method = "oxidized"
        if method == "" and (type(locations) == list or type(locations) == str) and rancid_base != "":
            method = "rancid"

        if method == "oxidized":
            self.__method = "oxidized"
            self.__base_url = oxidized_url
        elif method == "rancid":
            self.__method = "rancid"
            self.__locations = locations
            self.__rancid_base = rancid_base
        else:
            raise ValueError("Could not determine config method")
    # __init__

    # overwrite with functions from implementations
    def getActiveDevices(self):
        pass
    # getActiveDevices

    def getRouter(self, device):
        pass
    # getRouter

    def getConfig(self, device):
        pass
    # getConfig

    # generic functions, implement here

    def __str__(self):
        foo = "configuration:\n"
        foo = foo + "method:      "+self.__method+"\n"
        foo = foo + "base url:    "+self.__base_url+"\n"
        foo = foo + "locations:   "+str(self.__locations)+"\n"
        foo = foo + "rancid base: "+self.__rancid_base+"\n"
        return foo
    # __str__

    def filterActiveDevices(self, filter=""):
        pass
    # filterActiveDevices

    def printableInterfaceList(self, device):
        pass
    # printableInterfaceList

    def interfaceDescriptionList(self, device):
        pass
    # interfaceDescriptionList

    def interfaceAddressList(self, device, with_subnetsize=None):
        pass
    # interfaceAddressList

    def interfaceVrfList(self, device):
        pass
    # interfaceVrfList

    def printFilterSection(self, config, filterstr):
        pass
    # printFilterSection

    def printSection(self, vendor, sectionconfig):
        pass
    # printSection
# rtconfig

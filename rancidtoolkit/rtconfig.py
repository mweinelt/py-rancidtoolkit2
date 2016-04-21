#!/usr/bin/env python
#
# Written by Marcus Stoegbauer <ms@man-da.de>

"""
"""
import sys
import re
import os.path
from rancidtoolkit2.oxidized import oxidized 
from rancidtoolkit2.rancid import rancid

class rtconfig(object):

    __method = ""
    __configobj = None

    def __init__(self, method="", locations=None, rancid_base="", oxidized_url=""):
        if method == "" and oxidized_url != "":
            method = "oxidized"
        if method == "" and (type(locations) == list or type(locations) == str) and rancid_base != "":
            method = "rancid"

        if method == "oxidized":
            self.__method = "oxidized"
            self.__configobj = oxidized(oxidized_url=oxidized_url)
        elif method == "rancid":
            self.__method = "rancid"
            self.__configobj = rancid(locations=locations, rancid_base=rancid_base)
        else:
            raise ValueError("Could not determine config method")
    # __init__

    def getActiveDevices(self):
        if self.__method == "" or self.__configobj == None:
            raise LookupError("class not initialized")

        return self.__configobj.getActiveDevices()
    # getActiveDevices

    def filterActiveDevices(self, filter=""):
        if self.__method == "" or self.__configobj == None:
            raise LookupError("class not initialized")

        return self.__configobj.filterActiveDevices(filter)
    # filterActiveDevices

    def getRouter(self, device):
        if self.__method == "" or self.__configobj == None:
            raise LookupError("class not initialized")

        return self.__configobj.getRouter(device)
    # getRouter

    def getConfig(self, device):
        if self.__method == "" or self.__configobj == None:
            raise LookupError("class not initialized")

        return self.__configobj.getConfig(device)
    # getConfig

    def printableInterfaceList(self, device):
        if self.__method == "" or self.__configobj == None:
            raise LookupError("class not initialized")

        return self.__configobj.printableInterfaceList(device)
    # printableInterfaceList

    def interfaceDescriptionList(self, device):
        if self.__method == "" or self.__configobj == None:
            raise LookupError("class not initialized")

        return self.__configobj.interfaceDescriptionList(device)
    # interfaceDescriptionList

    def interfaceAddressList(self, device, with_subnetsize=None):
        if self.__method == "" or self.__configobj == None:
            raise LookupError("class not initialized")

        return self.__configobj.interfaceAddressList(device, with_subnetsize)
    # interfaceAddressList

    def interfaceVrfList(self, device):
        if self.__method == "" or self.__configobj == None:
            raise LookupError("class not initialized")

        return self.__configobj.interfaceVrfList(device)
    # interfaceVrfList

    def printFilterSection(self, config, filterstr):
        if self.__method == "" or self.__configobj == None:
            raise LookupError("class not initialized")

        return self.__configobj.printFilterSection(config, filterstr)
    # printFilterSection

    def printSection(self, vendor, sectionconfig):
        if self.__method == "" or self.__configobj == None:
            raise LookupError("class not initialized")

        return self.__configobj.printSection(vendor, sectionconfig)
    # printSection
# rtconfig

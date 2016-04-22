#!/usr/bin/env python
#
# Written by Marcus Stoegbauer <ms@man-da.de>

"""
"""
import sys
import re
import os.path
from . import cisco
from . import juniper

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

        if method != "oxidized" and method != "rancid":
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

    def filterActiveDevices(self, filter=None):
        devices = self.getActiveDevices()
        if type(filter) == dict:
            if 'vendor' in filter:
                filterdev = devices.copy()
                for dev in devices.keys():
                    if devices[dev].lower() != filter['vendor'].lower():
                        filterdev.pop(dev)
                # for dev
                devices = filterdev.copy()
            # if vendor
            if 'name' in filter:
                filterdev = devices.copy()
                for dev in devices.keys():
                    if not re.search(filter['name'], dev):
                        filterdev.pop(dev)
                # for dev
                devices = filterdev.copy()
            # if name
        else:
            raise TypeError("filter is not a dict")

        return devices.keys()
    # filterActiveDevices

    def printableInterfaceList(self, device):
        intlist = self.interfaceDescriptionList(device)

        ret = []
        for interface in intlist.keys():
            unit = ""
            unitre = re.search("(\.[0-9]+)$", interface)
            inttemp = interface
            if unitre:
                unit = unitre.group(1)
                inttemp = re.sub(".[0-9]+$", "", interface)
            # if unit
            lastintid = re.search("^(.*)/([0-9])$", inttemp)
            if lastintid:
                intstr = lastintid.group(1) + "/" + lastintid.group(2)
            else:
                intstr = inttemp
            # if lastintid
            if unit:
                intstr = intstr + unit
            # if unit
            ret.append(intstr + ": " + intlist[interface])
        # for interface
        ret.sort()
        return ret
    # printableInterfaceList

    def interfaceDescriptionList(self, device):
        devinfo = self.getRouter(device)
        if len(devinfo) == 0:
            raise LookupError("Could not find device %s" % device)

        devconfig = self.getConfig(devinfo[0])
        routertype = devinfo[1].lower()
        if routertype == "cisco" or routertype == "force10":
            return cisco.interfaces(devconfig)
        elif routertype == "juniper":
            return juniper.interfaces(devconfig)
        else:
            raise ValueError("Cannot handle device type %s for device %s." % (routertype, device))
        # if routertype
    # interfaceDescriptionList

    def interfaceAddressList(self, device, with_subnetsize=None):
        devinfo = self.getRouter(device)
        if len(devinfo) == 0:
            raise LookupError("Could not find device %s" % device)

        devconfig = self.getConfig(devinfo[0])
        routertype = devinfo[1].lower()
        if routertype == "cisco" or routertype == "force10":
            return cisco.addresses(devconfig, with_subnetsize)
        elif routertype == "juniper":
            return juniper.addresses(devconfig, with_subnetsize)
        else:
            raise ValueError("Cannot handle device type %s for device %s." % (routertype, device))
        # if routertype
    # interfaceAddressList

    def interfaceVrfList(self, device):
        devinfo = self.getRouter(device)
        if len(devinfo) == 0:
            raise LookupError("Could not find device %s" % device)

        devconfig = self.getConfig(devinfo[0])
        routertype = devinfo[1].lower()
        if routertype == "cisco" or routertype == "force10":
            return cisco.vrf(devconfig, with_subnetsize)
        else:
            raise ValueError("Cannot handle device type %s for device %s." % (routertype, device))
        # if routertype
    # interfaceVrfList

    def printFilterSection(self, device, filterstr):
        devinfo = self.getRouter(device)
        if len(devinfo) == 0:
            raise LookupError("Could not find device %s" % device)

        devconfig = self.getConfig(devinfo[0])
        routertype = devinfo[1].lower()
        if routertype == "cisco" or routertype == "force10":
            sections = cisco.section(devconfig, ".* ".join(filterstr))
            cisco.printSection(sections)
        elif routertype == "juniper":
            sections = juniper.section(devconfig, filterstr)
            juniper.printSection(sections)
        else:
            raise ValueError("Cannot handle device type %s for device %s." % (routertype, device))
        # if routertype

    # printFilterSection

    def printSection(self, vendor, sectionconfig):
        if vendor == "cisco" or vendor == "force10":
            cisco.printSection(sectionconfig)
        elif vendor == "juniper":
            juniper.printSection(sectionconfig)
        else:
            raise ValueError("Cannot handle device type %s for device %s." % (routertype, device))
        # if vendor
    # printSection
# rtconfig

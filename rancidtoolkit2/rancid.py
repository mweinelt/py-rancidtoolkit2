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
    __separator = ":"

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
        self.__method = "rancid"
        self.__locations = locations
        self.__rancid_base = rancid_base
        self.__setSeparator()
    # __init

    def __readRouterDb(self):
        """ reads all available router.db files and returns result as list """
        ret = list()
        for loc in self.__locations:
            hand = False
            routerdb = self.__rancid_base + "/" + loc + "/" + "/router.db"
            try:
                hand = open(routerdb)
            except:
                continue
            for line in hand:
                line = line[:-1].lower()
                if line == "" or re.match("^#", line) or \
                        re.match("^\s+$", line):
                    continue
                ret.append(line + ":" + loc)
            # for file
        # for locations
        return ret
    # __readRouterDb

    def __setSeparator(self):
        devs = self.__readRouterDb()
        if devs[0].find(";") > 0:
            self.__separator = ";"
    # __setSeparator

    def getActiveDevices(self):
        ret = dict()
        devs = self.__readRouterDb()
        for dev in devs:
            linesplit = dev.split(self.__separator)
            if len(linesplit) < 2:
                raise ValueError("separator `%s` in router.db entry not found:\n%s " % (self.__separator, dev))
            if linesplit[2] == "up":
                ret.update({linesplit[0]: linesplit[1]})
        return ret
    # getActiveDevices

    def getRouter(self, device):
        devs = self.__readRouterDb()
        for dev in devs:
            if re.match("^"+device, dev):
                ret = dev.split(self.__separator)
                return ret[0:2] + [ret[3]]
        # for dev
        return []
    # getRouter

    def getFilename(self, device):
        rancidentry = self.getRouter(device)
        if len(rancidentry) == 0:
            raise ValueError("Could not find device %s in rancid config" % device)

        filename = self.__rancid_base + "/" + rancidentry[2] + "/configs/" + rancidentry[0]
        if os.path.isfile(filename):
            fh = open(filename)
            firstline = fh.readline()
            fh.close()
        else:
            raise IOError("Filename %s for device %s is no file" % (filename, device))

        typere = re.search("RANCID-CONTENT-TYPE: (\w+)", firstline)
        if typere:
            routertype = typere.group(1)
        else:
            raise ValueError("Filename %s is not a saved configuration from rancid" % filename)
        return [filename, routertype]
    # getFileName


    def getConfig(self, device):
        filename = self.getFilename(device)
        hand = open(filename[0])
        lines = [line.rstrip('\n') for line in hand]
        hand.close()
        return lines
    # getConfig

# class rancid

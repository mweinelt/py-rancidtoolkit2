#!/usr/bin/env python
#
# Written by Marcus Stoegbauer <ms@man-da.de>

"""
"""
import sys
import re
import os.path
import requests, json
from rtconfig import rtconfig

class oxidized(rtconfig):

    __model_translate = {'ios': 'cisco', 'junos': 'juniper', 'screenos': 'netscreen', 'ftos': 'force10'}

    def __init__(self, oxidized_url=""):
        if type(oxidized_url) != str or oxidized_url == "":
            if sys.platform == "darwin":
                oxidized_url = "http://dazzle.office.man-da.de:8888"
        self.__method = "oxidized"
        self.__base_url = oxidized_url
    # __init

    def __translate_model(self, model):
        model = model.lower()
        if model in self.__model_translate:
            return self.__model_translate[model]
        else:
            return model
        # if
    # def __translate_model

    def getActiveDevices(self):
        """ dict: {'routername': 'model'}
        """
        resp = requests.get(self.__base_url + "/nodes.json")

        if not resp.ok:
            raise LookupError("Error getting nodes list: %s" % resp.reason)

        ret = dict()
        for node in resp.json():
            ret.update({node['name']: self.__translate_model(node['model'])})
        # for node
        return ret
    # getActiveDevices

    def getRouter(self, device):
        """ ['hostname', 'devicetype', 'group']
        """
        devs = self.getActiveDevices()
        for dev in devs:
            if re.match("^"+device, dev):
                resp = requests.get(self.__base_url + "/node/show/" + dev + ".json")
                if resp.ok:
                    data = resp.json()
                    return [str(dev), devs[dev], str(data['group'])]
                # if resp
            # if match
        # for dev
        return []
    # getRouter

    def getConfig(self, device):
        """ config as list()
        """
        oxentry = self.getRouter(device)
        if len(oxentry) == 0:
            raise ValueError("Could not find device %s in rancid config" % device)

        resp = requests.get(self.__base_url + "/node/fetch/" + oxentry[2] + "/" + oxentry[0])
        lines = [line.rstrip('\n') for line in resp.iter_lines()]
        return lines
    # getConfig
# class oxidized
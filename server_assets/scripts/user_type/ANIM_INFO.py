# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TAnimInfo(list):

    def __init__(self):
        list.__init__(self)

    def asDict(self):
        Data = {
            "Speed" : self[0],
            "Direction" : self[1],
        }
        return Data

    def createFromDict(self, DictData):
        self.extend([DictData["Speed"], DictData["Direction"]])
        return self

class ANIM_INFO_PICKLER:

    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        return TAnimInfo().createFromDict(dict)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TAnimInfo)

AnimInfoInst = ANIM_INFO_PICKLER()
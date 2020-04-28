# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TCombatInfo(list):

    def __init__(self):
        list.__init__(self)

    def asDict(self):
        Data = {
            "Name" : self[0],
            "RoleType" : self[1],
            "Point" : self[2],
            "Kill" : self[3],
            "Death" : self[4],
            "Assist" : self[5],
            "Ping" : self[6],
            "State" : self[7]
        }
        return Data

    def createFromDict(self, DictData):
        self.extend([DictData["Name"], DictData["RoleType"], DictData["Point"], DictData["Kill"], DictData["Death"], DictData["Assist"], DictData["Ping"], DictData["State"]])
        return self

#COMBAT_INFO序列化和反序列化
class COMBAT_INFO_PICKLER:

    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        return TCombatInfo().createFromDict(dict)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TCombatInfo)

CombatInfoInst = COMBAT_INFO_PICKLER()

class TCombatList(dict):

    def __init__(self):
        dict.__init__(self)

    def asDict(self):
        Data = []

        for key, val in self.items():
            Data.append(val)

        Dict = {"Value" : Data}

        return Dict

    def createFromDict(self, DictData):
        for data in DictData["Value"]:
            Prop = {"Name" : data[0], "RoleType" : data[1], "Point" : data[2], "Kill" : data[3], "Death" : data[4], "Assist" : data[5], "Ping" : data[6], "State" : data[7]}
            # 键 : 数据库id  --> 值 : TCombatInfo
            self[data[0]] = CombatInfoInst.createObjFromDict(Prop)
        return self

class COMBAT_LIST_PICKLER:

    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        return TCombatList().createFromDict(dict)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TCombatList)
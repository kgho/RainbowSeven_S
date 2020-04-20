# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TRoleInfo(list):

    def __init__(self):
        list.__init__(self)

    def asDict(self):
        Data = {
            "Dbid" : self[0],
            "RoleType" : self[1],
            "IsLock" : self[2],
            "Kill" : self[3],
            "Death" : self[4],
            "Assist" : self[5],
            "Point" : self[6],
            "PlayCount" : self[7]
        }
        return Data

    def createFromDict(self, DictData):
        self.extend([DictData["Dbid"], DictData["RoleType"], DictData["IsLock"], DictData["Kill"], DictData["Death"], DictData["Assist"], DictData["Point"], DictData["PlayCount"]])
        return self

#ROLE_INFO序列化和反序列化
class ROLE_INFO_PICKLER:

    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        return TRoleInfo().createFromDict(dict)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TRoleInfo)

RoleInfoInst = ROLE_INFO_PICKLER()

# 每个账户都有一个干员信息列表
class TRoleList(dict):

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
            Prop = {"Dbid" : data[0], "RoleType" : data[1], "IsLock" : data[2], "Kill" : data[3], "Death" : data[4], "Assist" : data[5], "Point" : data[6], "PlayCount" : data[7]}
            # 键 : 数据库id  --> 值 : TRoleInfo
            self[data[0]] = RoleInfoInst.createObjFromDict(Prop)
        return self

class ROLE_LIST_PICKLER:

    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        return TRoleList().createFromDict(dict)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TRoleList)

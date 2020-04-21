# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TPlayerInfo(list):

    def __init__(self):
        list.__init__(self)

    def asDict(self):
        Data = {
            "Name" : self[0],
            "Level" : self[1],
            "State" : self[2],
            "Avatar" : self[3],
            "Master" : self[4]
        }
        return Data

    def createFromDict(self, DictData):
        self.extend([DictData["Name"], DictData["Level"], DictData["State"], DictData["Avatar"], DictData["Master"]])
        return self

#PLAYER_INFO序列化和反序列化
class PLAYER_INFO_PICKLER:

    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        return TPlayerInfo().createFromDict(dict)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TPlayerInfo)

PlayerInfoInst = PLAYER_INFO_PICKLER()

# 每个房间都有一个玩家信息列表
class TPlayerList(dict):

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
            Prop = {"Name" : data[0], "Level" : data[1], "State" : data[2], "Avatar" : data[3], "Master" : data[4]}
            # 键 : 数据库id  --> 值 : TPlayerInfo
            self[data[0]] = PlayerInfoInst.createObjFromDict(Prop)
        return self

class PLAYER_LIST_PICKLER:

    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        return TPlayerList().createFromDict(dict)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TPlayerList)
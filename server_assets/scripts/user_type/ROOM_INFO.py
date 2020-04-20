# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TRoomInfo(list):
    def __init__(self):
        list.__init__(self)

    def asDict(self):
        Data = {
                "RoomId" : self[0],
                "Name" : self[1],
        }
        return Data

    def createFromDict(self, DictData):
        self.extend([DictData["RoomId"], DictData["Name"]])
        return self

#RoomInfo序列化和反序列化
class ROOM_INFO_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        return TRoomInfo().createFromDict(dict)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TRoomInfo)

RoomInfoInst = ROOM_INFO_PICKLER()

#房间信息列表
class TRoomList(dict):
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
            Prop = {"RoomId" : data[0], "Name" : data[1]}
            # key : 房间ID, value : TRoomInfo
            self[data[0]] = RoomInfoInst.createObjFromDict(Prop)

class ROOM_LIST_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        return TRoomList().createFromDict(dict)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TRoomList)
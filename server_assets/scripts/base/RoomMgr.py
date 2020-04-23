# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ROOM_INFO import TRoomInfo, TRoomList
from Room import Room
import time

class RoomMgr(KBEngine.Entity):
    """
    Room的房间管理器
    """
    def __init__(self):
        KBEngine.Entity.__init__(self)
        # 将RoomMgr存储在globalData中，方便获取
        KBEngine.globalData["RoomMgr"] = self

        # 存储所有Room的base实体 在 RoomList 字典中 ，id 作为 eky
        self.RoomList = {}

        # 正在创建中的房间字典，key ： 房间名  value ： Account
        # 从CreateRoom 到回调 OnRoomGetCell 需要时间，所以这段时间间隔内可能有多个同名的房间正在创建
        self.DemandAccount = {}

        # 自动创建两个默认房间
        # Props = {"Name" : self.__ACCOUNT_NAME__, "Time" : time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()), "Msg" : Msg}
        self.CreateRoom("服务器自动创建--肃清模式--木屋_1  "+time.strftime("%Y/%m/%d %H:%M:%S ", time.localtime()), None)
        # self.CreateRoom("服务器自动创建--肃清模式--木屋_2  "+time.strftime("%Y/%m/%d %H:%M:%S ", time.localtime()), None)


    def CreateRoom(self, Name, Account):
        """
        Name : 房间名
        Account : 有Account创建房间,然后交给角色实体？
        """
        # 查看是否有同名房间
        for RoomId, Room in self.RoomList.items():
            if Room.Name == Name:
                if Account is not none:
                    # 告诉账户已经有同名的房间
                    Account.OnAccountReqCreateRoom(False, 0, Name)
                return

        # 判断是否有正在创建中的同名房间请求
        if Name in self.DemandAccount:
            Account.OnAccountReqCreateRoom(False, 0, Name)
            return

        if Account is not None:
            # 将亲贵创建的房间名和账户保存
            self.DemandAccount[Name] = Account

        # 创建房间
        Props = {
        "Name" : Name
        }
        KBEngine.createEntityLocally("Room", Props)


    def OnRoomGetCell(self, Room):
        """
        创建房间cell实体生成回调函数
        创建出cell实体的房间的base实体
        """
        # 房间创建出cell实体后才能添加到房间列表
        self.RoomList[Room.id] = Room

        for Name, Account in self.DemandAccount.items():
            # 找到创建成功房间对应的账户，通知账户创建成功
            if Name == Room.Name:
                Account.OnAccountReqCreateRoom(True, Room.id, Room.Name)
                # 从字典移除
                del self.DemandAccount[Name]
                return


    def OnRoomLoseCell(self, RoomId):
        """
        创建房间cell实体生成回调函数
        房间ID
        """
        del self.RoomList[RoomId]

    def GetRoomList(self):
        """
        获取房间列表
        """
        # 该脚本中RoomList是一个字典
        # 发给客户端要转换为网络传输使用的类型
        RoomList = TRoomList()
        for RoomId, Room in self.RoomList.items():
            Props = {"RoomId" : RoomId, "Name" : Room.Name}
            RoomList[RoomId] = TRoomInfo().createFromDict(Props)
        return RoomList

    def EnterRoom(self, EntityAccount, RoomId):
        """
        账户进入RoomId对应的房间
        """
        # 根据房间ID,得到Room实体
        Room = self.RoomList[RoomId]
        if Room is None:
            ERROR_MSG("RoomMgr::EnterRoom: Room with Id(%i) is none" % (RoomId))
            return
        Room.Enter(EntityAccount)

    def LeaveRoom(self, EntityId, RoomId):
        """
        账户离开房间
        """
        ERROR_MSG("RoomMgr::LeaveRoom:")
        # 根据房间ID,得到Room实体
        Room = self.RoomList[RoomId]
        if Room is None:
            ERROR_MSG("RoomMgr::LeaveRoom: Room with Id(%i) is none" % (RoomId))
            return
        Room.Leave(EntityId)

    def PlayerChangeState(self, EntityId, RoomId, state):
        """
        玩家修改状态
        """
        ERROR_MSG("RoomMgr::PlayerChangeState:")
        # 根据房间ID,得到Room实体
        Room = self.RoomList[RoomId]
        if Room is None:
            ERROR_MSG("RoomMgr::LeaveRoom: Room with Id(%i) is none" % (RoomId))
            return
        Room.PlayerChangeState(EntityId, state)

    def RoomEnterGame(self, RoomId, code):
        Room = self.RoomList[RoomId]
        Room.EnterGame(code)
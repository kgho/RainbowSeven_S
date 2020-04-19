# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ROOM_INFO import TRoomInfo, TRoomList
from Room import Room

class RSOperator(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        # 将RoomMgr存储在globalData中，方便获取
        KBEngine.globalData["RoomMgr"] = self

        # 存储所有Room的base实体 在 RoomList 字典中 ，id 作为索引
        self.RoomList = {}

        # 正在创建中的房间字典，key ： 房间名  value ： Account
        # 从CreateRoom 到回调 OnRoomGetCell 需要时间，所以这段时间间隔内可能有多个同名的房间正在创建
        self.DemandAccount = {}

        # 自动创建两个默认房间
        self.CreateRoom("自动创建-肃清模式-木屋_1", None)
        self.CreateRoom("自动创建-肃清模式-木屋_2", None)


    def CreateRoom(self, Name, Account)
        """
        Name : 房间名
        Account : 有Account创建房间,然后交给角色实体？
        """
        # 查看是否有同名房间
        for RoomId, Room in self.RoomList.items():
            if Room.Name == Name:
                if Account is not none:
                    # 告诉账户已经有同名的房间
                    Account.OnAcountCreateRoom(False, 0, Name)
                return

        # 判断是否有正在创建中的同名房间请求
        if Name in self.DemandAccount:
            Account.OnAcountCreateRoom(False, 0, Name)
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
            if Name == Room.Name
                Account.OnAcountCreateRoom(True, Room.id, Room.Name)
                # 从字典移除
                del self.DemandAccount[Name]
                return


    def OnRoomLoseCell(self, RoomId):
        """
        创建房间cell实体生成回调函数
        房间ID
        """
        del self.RoomList[RoomId]
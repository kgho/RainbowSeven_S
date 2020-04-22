# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from PLAYER_INFO import TPlayerInfo, TPlayerList

class Room(KBEngine.Space):
    """
    Room的base部分
    注意：它不是一个实体，并不是真正的space
    真的的space存在于cellapp内存中
    通过这个实体与之关联并操纵space
    """
    def __init__(self):
        KBEngine.Space.__init__(self)

        # 账户字典， key 实体ID ， value base实体 ，cell实体不考虑
        self.EntityDict = {}
        # 玩家信息字典,玩家名称作为 key, 玩家信息作为 value
        # 玩家分为 蓝 红 两队,每队最多5名玩家
        self.PlayerListBlue = {}
        self.PlayerListRed = {}

        # 房主在字典的 key
        self.masterEntityKey = 0

    def Enter(self, EntityAccount):
        """
        # 进入房间
        # EntityAccount : 进入房间的Entity 的 Base 实体
        """
        ERROR_MSG("Room::Enteroom: Name %s" % EntityAccount.__ACCOUNT_NAME__)

        # 客户端在房间直接退出游戏了，cell实体还没来得及销毁，此时不能进入房间
        if EntityAccount.cell is not None:
            PlayerListBlue = TPlayerList()
            for Name, Player in self.PlayerListBlue.items():
                Props = {"Name" : Player[0], "Level" : Player[1], "State" : Player[2], "Avatar" : Player[3], "Master" : Player[4]}
                PlayerListBlue[Name] = TPlayerInfo().createFromDict(Props)

            PlayerListRed = TPlayerList()
            for Name, Player in self.PlayerListRed.items():
                Props = {"Name" : Player[0], "Level" : Player[1], "State" : Player[2], "Avatar" : Player[3], "Master" : Player[4]}
                PlayerListRed[Name] = TPlayerInfo().createFromDict(Props)

            EntityAccount.client.OnReqEnterRoom(1, PlayerListBlue, PlayerListRed)
            ERROR_MSG("Room::Enteroom: Failed %i." % EntityAccount.id)
            return

        ERROR_MSG("Room::Enteroom: Successful %i." % EntityAccount.id)

        # 假设当前玩家是房主
        isMaster = 1

        # 蓝队是否有房主
        for AccountName,PlayerInfo in self.PlayerListBlue.items():
            if PlayerInfo[4] == 1:
                isMaster = 0

        # 红队是否有房主
        for AccountName,PlayerInfo in self.PlayerListRed.items():
            if PlayerInfo[4] == 1:
                isMaster = 0

        if isMaster == 1:
            self.masterEntityKey = EntityAccount.id

        Props = {"Name" : EntityAccount.__ACCOUNT_NAME__, "Level" : EntityAccount.Level, "State" : 0, "Avatar" : 0, "Master" : isMaster}

        if len(self.PlayerListBlue) <= len(self.PlayerListRed):
            if len(self.PlayerListBlue)<5:
                self.PlayerListBlue[EntityAccount.__ACCOUNT_NAME__] = TPlayerInfo().createFromDict(Props)
            else:
                self.returnOnReqEnterRoomFull(EntityAccount)
                return
        else:
            if len(self.PlayerListRed) < 5:
                self.PlayerListRed[EntityAccount.__ACCOUNT_NAME__] = TPlayerInfo().createFromDict(Props)
            else:
                self.returnOnReqEnterRoomFull(EntityAccount)
                return

        # 将进入的实体保存到玩家字典
        ERROR_MSG("Room::Enteroom: EntityDictCount %i" % len(self.EntityDict))

        self.EntityDict[EntityAccount.id] = EntityAccount

        # 进入的玩家未准备,通知房主不能开始游戏
        self.EntityDict[self.masterEntityKey].client.OnAllReady(1)

        for ID, Account in self.EntityDict.items():
            Account.client.OnReqEnterRoom(0, self.returnPlayerList(self.PlayerListBlue), self.returnPlayerList(self.PlayerListRed))

        # 把实体放入房间的cell空间，调用 self.cell.OnEnter(EntityRole) 也可
        EntityAccount.createCellEntity(self.cell)

    def Leave(self, EntityId):
        """
        # 离开房间(Base实体离开)，如果存在cell实体，也要删除
        """
        ERROR_MSG("Room::Leave:")
        # 获取玩家
        EntityAccount = self.EntityDict[EntityId]

        # 要删除的玩家名称,离开房间的是否是房主
        delPlayerName = ""
        isBlue = True
        isMaster = 0

        for Name, Player in self.PlayerListBlue.items():
            if Name == EntityAccount.__ACCOUNT_NAME__:
                delPlayerName = Name
                isMaster = Player[4]

        for Name, Player in self.PlayerListRed.items():
            if Name == EntityAccount.__ACCOUNT_NAME__:
                delPlayerName = Name
                isBlue = False
                isMaster = Player[4]

        ERROR_MSG("Room::Leave--> Name:%s , isBlue:%s" % (delPlayerName, isBlue))

        if isBlue:
            del self.PlayerListBlue[delPlayerName]
        else:
            del self.PlayerListRed[delPlayerName]

        # 把玩家移除字典
        del self.EntityDict[EntityId]

        # 如果离开的是房主，让列表里第一名玩家成为房主
        if isMaster == 1:
            if len(self.PlayerListBlue) > 0:
                result=[]
                for k,v in self.PlayerListBlue.items():
                    result.append(k)
                self.PlayerListBlue[result[0]][4] = 1
                ERROR_MSG("Room::Leave--> BlueTeam:%s is Master." % result[0])

                for ID, Account in self.EntityDict.items():
                    if Account.__ACCOUNT_NAME__ == result[0]:
                        self.masterEntityKey = ID

            elif len(self.PlayerListRed) > 0:
                result=[]
                for k,v in self.PlayerListRed.items():
                    result.append(k)
                self.PlayerListRed[result[0]][4] = 1
                ERROR_MSG("Room::Leave--> RedTeam:%s is Master." % result[0])

                for ID, Account in self.EntityDict.items():
                    if Account.__ACCOUNT_NAME__ == result[0]:
                        self.masterEntityKey = ID

        # 有玩家退出了,通知其它玩家更新房间玩家信息
        for ID, Account in self.EntityDict.items():
            if EntityAccount.__ACCOUNT_NAME__ != Account.__ACCOUNT_NAME__:
                Account.client.OnReqEnterRoom(0, self.returnPlayerList(self.PlayerListBlue), self.returnPlayerList(self.PlayerListRed))

        # 一个未准备的玩家退出后可能就全员准备了
        if len(self.EntityDict) > 0:
            self.isAllReady()

        # 销毁玩家cell实体
        # 如果base实体不为空
        if EntityAccount is not None:
            # 如果cell实体不为空
            if EntityAccount.cell is not None:
                #通过base 实体调用方法 销毁 cell 实体 (销毁后回调该实体的 OnLose方法)
                EntityAccount.destroyCellEntity()

    def onGetCell(self):
        """
        # Room 的cell 部分创建成功回调
        """
        # 通知RoomMgr，房间创建成功,self是参数，Room的实体
        KBEngine.globalData["RoomMgr"].OnRoomGetCell(self)

    def onLoseCell(self):
        """
        # Room 的cell 部分销毁成功回调
        """
        # 通知RoomMgr，房间销毁
        KBEngine.globalData["RoomMgr"].OnRoomGetCell(self)
        # 销毁cell实体，同时销毁base实体？
        self.destroy()

    def returnOnReqEnterRoomFull(self, EntityAccount):
        PlayerListBlue = TPlayerList()
        for Name, Player in self.PlayerListBlue.items():
            Props = {"Name" : Player[0], "Level" : Player[1], "State" : Player[2], "Avatar" : Player[3], "Master" : Player[4]}
            PlayerListBlue[Name] = TPlayerInfo().createFromDict(Props)

        PlayerListRed = TPlayerList()
        for Name, Player in self.PlayerListRed.items():
            Props = {"Name" : Player[0], "Level" : Player[1], "State" : Player[2], "Avatar" : Player[3], "Master" : Player[4]}
            PlayerListRed[Name] = TPlayerInfo().createFromDict(Props)

        EntityAccount.client.OnReqEnterRoom(2, PlayerListBlue, PlayerListRed)
        ERROR_MSG("Room::Enteroom: Full.")

    def returnPlayerList(self, PlayerList):
        tempPlayerList = TPlayerList()
        for Name, Player in PlayerList.items():
            Props = {"Name" : Player[0], "Level" : Player[1], "State" : Player[2], "Avatar" : Player[3], "Master" : Player[4]}
            tempPlayerList[Name] = TPlayerInfo().createFromDict(Props)
        ERROR_MSG("Room::Enteroom: returnPlayerList:%i" % len(tempPlayerList))
        return tempPlayerList

    def PlayerChangeState(self, EntityId, state):
        EntityAccount = self.EntityDict[EntityId]
        # 改变状态的账户名
        accountName = EntityAccount.__ACCOUNT_NAME__

        # 存储该玩家状态到房间
        for k,v in self.PlayerListBlue.items():
            if k == accountName:
                v[2] = state
        for k,v in self.PlayerListRed.items():
            if k == accountName:
                v[2] = state

        # 有玩家状态改变,通知所有玩家更新
        for ID, Account in self.EntityDict.items():
            Account.client.OnReqEnterRoom(0, self.returnPlayerList(self.PlayerListBlue), self.returnPlayerList(self.PlayerListRed))

        EntityAccount.client.OnReqChangeState(state)

        self.isAllReady()

    def isAllReady(self):
        """
        返回是否所有玩家已准备
        """
        isAllReady = True
        for k,v in self.PlayerListBlue.items():
            if v[2] == 0:
                isAllReady = False
        for k,v in self.PlayerListRed.items():
            if v[2] == 0:
                isAllReady = False
        if isAllReady:
            # 通知房主客户端可以开始游戏了,当前1个玩家也可以开始游戏
            if len(self.EntityDict) > 0:
                self.EntityDict[self.masterEntityKey].client.OnAllReady(0)
        else:
            # 进入了未准备的玩家,不能开始游戏
            if len(self.EntityDict) > 0:
                self.EntityDict[self.masterEntityKey].client.OnAllReady(1)





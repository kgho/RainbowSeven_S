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
        self.AccountDict = {}

        # 玩家信息字典,  key,  实体ID   玩家信息作为 value
        # 玩家分为 蓝 红 两队,每队最多5名玩家
        # PlayerInfo 保存的是玩家在房间的数据，进入对战后不再改变。
        self.PlayerListBlue = {}
        self.PlayerListRed = {}

        # 玩家选择干员后的角色字典
        self.RoleEntityDict = {}

        # 房主在字典的 key
        self.masterEntityKey = 0

        # 该房间是否正在游戏，目前不能中途加入
        self.isInGame = False

    def AccountEnter(self, EntityAccount):
        """
        # 账户进入房间
        # EntityAccount : 进入房间的Entity 的 Base 实体
        """
        ERROR_MSG("Room::AccountEnter: Name %s" % EntityAccount.__ACCOUNT_NAME__)

        # 假设当前玩家是房主
        isMaster = 1

        # 蓝队是否有房主
        for ID,PlayerInfo in self.PlayerListBlue.items():
            if PlayerInfo[4] == 1:
                isMaster = 0

        # 红队是否有房主
        for ID,PlayerInfo in self.PlayerListRed.items():
            if PlayerInfo[4] == 1:
                isMaster = 0

        if isMaster == 1:
            self.masterEntityKey = EntityAccount.id

        Props = {"Name" : EntityAccount.__ACCOUNT_NAME__, "Level" : EntityAccount.Level, "State" : 0, "Avatar" : 0, "Master" : isMaster}

        if len(self.PlayerListBlue) <= len(self.PlayerListRed):
            if len(self.PlayerListBlue)<5:
                self.PlayerListBlue[EntityAccount.id] = TPlayerInfo().createFromDict(Props)
            else:
                self.returnOnReqEnterRoomFull(EntityAccount)
                return
        else:
            if len(self.PlayerListRed) < 5:
                self.PlayerListRed[EntityAccount.id] = TPlayerInfo().createFromDict(Props)
            else:
                self.returnOnReqEnterRoomFull(EntityAccount)
                return

        # 将进入的实体保存到玩家字典
        ERROR_MSG("Room::Enteroom: EntityDictCount %i" % len(self.AccountDict))

        self.AccountDict[EntityAccount.id] = EntityAccount

        EntityAccount.isInRoom = True

        # 进入的玩家未准备,通知房主不能开始游戏
        self.AccountDict[self.masterEntityKey].client.OnAllReady(1)

        for ID, Account in self.AccountDict.items():
            Account.client.OnReqEnterRoom(0, self.returnPlayerList(self.PlayerListBlue), self.returnPlayerList(self.PlayerListRed))

        

    def AccountLeave(self, EntityId):
        """
        # 账户离开房间
        """
        ERROR_MSG("Room::AccountLeave:")
        # 获取玩家
        EntityAccount = self.AccountDict[EntityId]

        # 要删除的玩家名称,离开房间的是否是房主
        delPlayerID = ""
        isBlue = True
        isMaster = 0

        for ID, Player in self.PlayerListBlue.items():
            if ID == EntityAccount.id:
                delPlayerID = ID
                isMaster = Player[4]

        for ID, Player in self.PlayerListRed.items():
            if ID == EntityAccount.id:
                delPlayerID = ID
                isBlue = False
                isMaster = Player[4]

        ERROR_MSG("Room::AccountLeave--> ID:%s , isBlue:%s" % (delPlayerID, isBlue))

        if isBlue:
            del self.PlayerListBlue[delPlayerID]
        else:
            del self.PlayerListRed[delPlayerID]

        self.AccountDict[EntityId].isInRoom = False

        # 把玩家移除字典
        del self.AccountDict[EntityId]

        # 如果离开的是房主，让列表里第一名玩家成为房主
        if isMaster == 1:
            if len(self.PlayerListBlue) > 0:
                result=[]
                for k,v in self.PlayerListBlue.items():
                    result.append(k)
                self.PlayerListBlue[result[0]][4] = 1
                ERROR_MSG("Room::Leave--> BlueTeam:%s is Master." % result[0])

                for ID, Account in self.AccountDict.items():
                    if Account.__ACCOUNT_NAME__ == result[0]:
                        self.masterEntityKey = ID

            elif len(self.PlayerListRed) > 0:
                result=[]
                for k,v in self.PlayerListRed.items():
                    result.append(k)
                self.PlayerListRed[result[0]][4] = 1
                ERROR_MSG("Room::Leave--> RedTeam:%s is Master." % result[0])

                for ID, Account in self.AccountDict.items():
                    if Account.__ACCOUNT_NAME__ == result[0]:
                        self.masterEntityKey = ID

        # 有玩家退出了,通知其它玩家更新房间玩家信息
        for ID, Account in self.AccountDict.items():
            if EntityAccount.id != Account.id:
                Account.client.OnReqEnterRoom(0, self.returnPlayerList(self.PlayerListBlue), self.returnPlayerList(self.PlayerListRed))

        # 一个未准备的玩家退出后可能就全员准备了
        if len(self.AccountDict) > 0:
            self.isAllReady()

        EntityAccount.client.OnReqLeaveRoom(0)

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
        for ID, Player in self.PlayerListBlue.items():
            Props = {"Name" : Player[0], "Level" : Player[1], "State" : Player[2], "Avatar" : Player[3], "Master" : Player[4]}
            PlayerListBlue[ID] = TPlayerInfo().createFromDict(Props)

        PlayerListRed = TPlayerList()
        for ID, Player in self.PlayerListRed.items():
            Props = {"Name" : Player[0], "Level" : Player[1], "State" : Player[2], "Avatar" : Player[3], "Master" : Player[4]}
            PlayerListRed[ID] = TPlayerInfo().createFromDict(Props)

        EntityAccount.client.OnReqEnterRoom(2, PlayerListBlue, PlayerListRed)
        ERROR_MSG("Room::Enteroom: Full.")

    def returnPlayerList(self, PlayerList):
        tempPlayerList = TPlayerList()
        for ID, Player in PlayerList.items():
            Props = {"Name" : Player[0], "Level" : Player[1], "State" : Player[2], "Avatar" : Player[3], "Master" : Player[4]}
            tempPlayerList[ID] = TPlayerInfo().createFromDict(Props)
        ERROR_MSG("Room::Enteroom: returnPlayerList:%i" % len(tempPlayerList))
        return tempPlayerList

    def PlayerChangeState(self, EntityId, state):
        EntityAccount = self.AccountDict[EntityId]
        # 改变状态的账户名
        ID = EntityAccount.id

        # 存储该玩家状态到房间
        for id,PlayerInfo in self.PlayerListBlue.items():
            if id == ID:
                v[2] = state
        for id,PlayerInfo in self.PlayerListRed.items():
            if id == ID:
                v[2] = state

        # 有玩家状态改变,通知所有玩家更新
        for ID, Account in self.AccountDict.items():
            Account.client.OnReqEnterRoom(0, self.returnPlayerList(self.PlayerListBlue), self.returnPlayerList(self.PlayerListRed))

        EntityAccount.client.OnReqChangeState(state)

        self.isAllReady()

    def Leave(self, EntityId):
        """
        # 离开房间(Base实体离开)，如果存在cell实体，也要删除
        """
        ERROR_MSG("Room::Leave:")
        # 获取玩家
        EntityAccount = self.AccountDict[EntityId]

        # 要删除的玩家ID,离开房间的是否是房主
        delPlayerID = ""
        isBlue = True
        isMaster = 0

        for ID, Player in self.PlayerListBlue.items():
            if ID == EntityAccount.id:
                delPlayerID = ID
                isMaster = Player[4]

        for ID, Player in self.PlayerListRed.items():
            if ID == EntityAccount.id:
                delPlayerID = ID
                isBlue = False
                isMaster = Player[4]

        ERROR_MSG("Room::Leave--> ID:%s , isBlue:%s" % (delPlayerID, isBlue))

        if isBlue:
            del self.PlayerListBlue[delPlayerID]
        else:
            del self.PlayerListRed[delPlayerID]

        # 把玩家移除字典
        del self.AccountDict[EntityId]

        # 如果离开的是房主，让列表里第一名玩家成为房主
        if isMaster == 1:
            if len(self.PlayerListBlue) > 0:
                result=[]
                for k,v in self.PlayerListBlue.items():
                    result.append(k)
                self.PlayerListBlue[result[0]][4] = 1
                ERROR_MSG("Room::Leave--> BlueTeam:%s is Master." % result[0])

                for ID, Account in self.AccountDict.items():
                    if Account.__ACCOUNT_NAME__ == result[0]:
                        self.masterEntityKey = ID

            elif len(self.PlayerListRed) > 0:
                result=[]
                for k,v in self.PlayerListRed.items():
                    result.append(k)
                self.PlayerListRed[result[0]][4] = 1
                ERROR_MSG("Room::Leave--> RedTeam:%s is Master." % result[0])

                for ID, Account in self.AccountDict.items():
                    if Account.__ACCOUNT_NAME__ == result[0]:
                        self.masterEntityKey = ID

        # 有玩家退出了,通知其它玩家更新房间玩家信息
        for ID, Account in self.AccountDict.items():
            if EntityAccount.__ACCOUNT_NAME__ != Account.__ACCOUNT_NAME__:
                Account.client.OnReqEnterRoom(0, self.returnPlayerList(self.PlayerListBlue), self.returnPlayerList(self.PlayerListRed))

        # 一个未准备的玩家退出后可能就全员准备了
        if len(self.AccountDict) > 0:
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
        for ID, Player in self.PlayerListBlue.items():
            Props = {"Name" : Player[0], "Level" : Player[1], "State" : Player[2], "Avatar" : Player[3], "Master" : Player[4]}
            PlayerListBlue[ID] = TPlayerInfo().createFromDict(Props)

        PlayerListRed = TPlayerList()
        for ID, Player in self.PlayerListRed.items():
            Props = {"Name" : Player[0], "Level" : Player[1], "State" : Player[2], "Avatar" : Player[3], "Master" : Player[4]}
            PlayerListRed[ID] = TPlayerInfo().createFromDict(Props)

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
        EntityAccount = self.AccountDict[EntityId]
        # 改变状态的账户 ID
        ID = EntityAccount.id

        # 存储该玩家状态到房间
        for k,v in self.PlayerListBlue.items():
            if k == ID:
                v[2] = state
        for k,v in self.PlayerListRed.items():
            if k == ID:
                v[2] = state

        # 有玩家状态改变,通知所有玩家更新
        for ID, Account in self.AccountDict.items():
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
            if len(self.AccountDict) > 0:
                self.AccountDict[self.masterEntityKey].client.OnAllReady(0)
        else:
            # 进入了未准备的玩家,不能开始游戏
            if len(self.AccountDict) > 0:
                self.AccountDict[self.masterEntityKey].client.OnAllReady(1)

    # 房主请求开始游戏，通知所有玩家游戏要开始了
    def StartGame(self, code):
        for ID, Account in self.AccountDict.items():
            ERROR_MSG("Room::StartGame: code %i" % code)
            Account.client.OnReqStartGame(code)

    def EnterGame(self, EntityRole):
        """
        # 进入游戏
        # :param EntityRole: 进入场景的Entity的Base实体
        """
        ERROR_MSG("Room::EnterGame")

        # 把实体放入房间的Cell空间 调用 self.cell.OnEnter(EntityRole) 也可以
        EntityRole.createCellEntity(self.cell)
        # 保存到角色字典
        self.RoleEntityDict[EntityRole.id] = EntityRole

    def QuitGame(self, AccountID, EntityRole):
        """
        # 退出游戏
        # :param EntityRole: 退出游戏场景的Entity的Base实体
        """
        ERROR_MSG("Room::QuitGame")

        self.AccountDict[AccountID].isInRoom = False
        self.AccountDict[AccountID].isInGame = False

        # 把玩家移出字典
        del self.AccountDict[AccountID]

        if self.PlayerListBlue.hsa_key():
            del self.PlayerListBlue[AccountID]

        if self.PlayerListRed.hsa_key():
            del self.PlayerListRed[AccountID]
        
        # 把玩家角色移出字典
        del self.RoleEntityDict[EntityRole.id]

        # 销毁玩家cell实体
        if EntityRole.cell is not None:
            EntityRole.destroyCellEntity()






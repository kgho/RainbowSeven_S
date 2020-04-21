# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ROLE_INFO import TRoleInfo, TRoleList
from ROOM_INFO import TRoomInfo

class Account(KBEngine.Proxy):
    def __init__(self):
        KBEngine.Proxy.__init__(self)

    def onTimer(self, id, userArg):
        """
        KBEngine method.
        使用addTimer后， 当时间到达则该接口被调用
        @param id       : addTimer 的返回值ID
        @param userArg  : addTimer 最后一个参数所给入的数据
        """
        DEBUG_MSG(id, userArg)

    def onClientEnabled(self):
        """
        KBEngine method.
        该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
        cell部分。
        """
        DEBUG_MSG("account[%i] entities. eneityCall:%s" %(self.id, self.client))

    def onLogOnAttempt(self, ip, port, password):
        """
        KBEngine method.
        客户端登陆失败时会回调到这里
        """
        INFO_MSG(ip, port, password)
        return KBEngine.LOG_ON_ACCEPT

    def onClientDeath(self):
        """
        KBEngine method.
        客户端对应实体已经销毁
        """
        ERROR_MSG("Account[%i].onClientDeath:" % self.id)
        # 如果cell存在，说明在房间中强退出了游戏
        if self.cell is not None:
            KBEngine.globalData["RoomMgr"].LeaveRoom(self.id, self.CurrentRoomID)
            return

        self.destroy()

    def ReqAccountInfo(self):
        """
        请求账户信息：等级，经验，声望值，金币
        """
        DEBUG_MSG("Account[%i]::ReqAccountInfo: Level=%i, Exp=%i, Fame=%i, Coin=%i." % (self.id, self.Level, self.Exp, self.Fame, self.Coin))

        self.client.OnReqAccountInfo(self.Level, self.Exp, self.Fame, self.Coin)

    def ReqRoleInfo(self, RoleType):
        """
        客户端请求干员信息
        """
        DEBUG_MSG("Account[%i]::ReqRoleInfo: RoleType=%i" % (self.id, RoleType))

        # 通过干员类型 从该账户干员列表中 找到对应干员
        for key, info in self.RoleList.items():
            if info[1] == RoleType:
                self.client.OnReqRoleInfo(info)

    def ReqRoleList(self):
        """
        客户端请求干员列表
        """
        DEBUG_MSG("Account[%i]::ReqRoleList: Size=%i." %(self.id, len(self.RoleList)))

        if(len(self.RoleList)>0):
            self.client.OnReqRoleList(self.RoleList)
        else:
            # 如果该账户没有角色自动解锁第一个干员
            DEBUG_MSG("Account[%i]::ReqRoleList:Unlock Role 001." %(self.id))
            self.ReqUnlockRole(1)
            DEBUG_MSG("Account[%i]::ReqRoleList: Size=%i." %(self.id, len(self.RoleList)))
            self.client.OnReqRoleList(self.RoleList)

    def ReqUnlockRole(self, RoleType):
        """
        客户端请求解锁干员
        RoleType : 干员类型
        """
        DEBUG_MSG("Account[%i]::ReqUnlockRole: RoleType=%i" % (self.id, RoleType))

        # 判断该类型干员是否已经解锁
        # 0:干员已解锁
        for key, info in self.RoleList.items():
            # 已存在 并 已解锁
            if info[1] == RoleType and info[2] == 1:
                self.client.OnReqUnlockRole(1, RoleType)
                DEBUG_MSG("Account[%i]::ReqUnlockRole: RoleType=%i Has Unlock." % (self.id, RoleType))
                return
            # 与存在 并 未解锁，解锁后返回
            if info[1] == RoleType and info[2] == 0:
                self.client.OnReqUnlockRole(2, RoleType)
                DEBUG_MSG("Account[%i]::ReqUnlockRole: RoleType=%i Unlock Angain." % (self.id, RoleType))
                return

        # 创建Role， 设置角色初始变量
        Props = {
            "RoleType" : RoleType,
            "IsLock" : 1,
            "Kill" : 0,
            "Death" : 0,
            "Assist" : 0,
            "Point" : 0,
            "PlayCount" : 0
        }
        Role = KBEngine.createEntityLocally('Role', Props)

        #将角色写入数据库， 在回调函数中通知客户端解锁并创建成功
        if Role:
            Role.writeToDB(self._OnRoleSaved)
        else:
            # 创建Role失败
            self.client.OnReqUnlockRole(3, RoleType)

    def _OnRoleSaved(self, Success, Role):
        """
        新建角色写入数据库回调
        Success : 是否写入成功
        Role : 写入数据库实体
        """
        # 如果账号已销毁，把角色从数据库删除
        if self.isDestroyed:
            if Role:
                # destroy方法内填入Ture会从数据库删除实体数据
                Role.destroy(True)
            return
        
        # 回调函数返回参数 角色
        RoleInfo = TRoleInfo()
        RoleInfo.extend([0, 0, 1, 0, 0, 0, 0, 0])
        if Role:
            # cellData可以获取未生成cell实体时cell作用域的变量
            RoleInfo[1] = Role.cellData["RoleType"]
            #判断是否写入数据库成功
            if Success:
                RoleInfo[0] = Role.databaseID
                # 将 Role 填入 RoleList
                self.RoleList[Role.databaseID] = RoleInfo
                # 通知客户端 解锁成功
                if self.client:
                    # 说明Role 新解锁干员信息 写入数据库成功
                    self.client.OnReqUnlockRole(0, RoleInfo[1])
                # 保存到数据库
                self.writeToDB()
            else:
                if self.client:
                    # 说明写入失败
                    self.client.OnReqUnlockRole(4, RoleInfo[1])
            # 销毁Role
            Role.destroy()
        else:
            if self.client:
                # 解锁失败
                self.client.self.client.OnReqUnlockRole(3, RoleInfo[1])

    def ReqRoomList(self):
        """
        客户端请求房间列表
        """
        RoomList = KBEngine.globalData["RoomMgr"].GetRoomList()
        DEBUG_MSG("Account[%i].ReqRoomList: RoomList = %s" % (self.id, RoomList.asDict()))
        self.client.OnReqRoomList(RoomList)

    def ReqCreateRoom(self, Name):  
        """
        客户端请求创建房间, 传入房间名字
        """
        DEBUG_MSG("Account[%i].ReqCreateRoom: RoomName = %s" % (self.id, Name))
        KBEngine.globalData["RoomMgr"].CreateRoom(Name, self)

    def OnAccountReqCreateRoom(self, Succeed, RoomId, Name):
        """
        创建房间的回调函数
        """
        Props = {"RoomId" : RoomId, "Name" : Name}
        RoomInfo = TRoomInfo().createFromDict(Props)

        if Succeed:
            self.client.OnReqCreateRoom(0, RoomInfo)
        else:
            self.client.OnReqCreateRoom(1, RoomInfo)

    def ReqEnterRoom(self, RoomId):
        """
        客户端请求进入房间
        """
        DEBUG_MSG("Account[%i].ReqEnterRoom: RoomId = %i " % (self.id, RoomId))
        # 保存当前所在房间id
        self.CurrentRoomID = RoomId
        # 账户进入房间
        KBEngine.globalData["RoomMgr"].EnterRoom(self, self.CurrentRoomID)

    def onGetCell(self):
        DEBUG_MSG("Account.Base[%i].onGetCell: " % (self.id))

    def onLoseCell(self):
        # cell实体销毁，说明强退客户端了，或退出房间了
        ERROR_MSG("Account[%i].onLoseCell:" % self.id)
        self.destroy()

    def ReqLeaveRoom(self):
        if self.cell is not None:
            ERROR_MSG("Account[%i].ReqLeaveRoom:" % self.id)



# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from CHAT_INFO import TChatInfo
import time #python包

class Account(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)

		#该变量保存该实体所在房间的ID
		self.CurrentRoomId = 0
		#要传送到的房间ID
		self.TeleportRoomId = 0

		#3分钟后销毁（模拟退出）
		#self.addTimer(60 *3, 0, 0)


	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)
		
	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		RoomMgr = KBEngine.globalData["RoomMgr"]
		RoomMgr.EnterRoom("房间_1", self)

	def ReqTeleport(self):
		"""
		cell实体传送请求
		"""
		#需要获取玩家所在房间的base实体ID
		KBEngine.globalData["RoomMgr"].TeleportRoom(self)

	def TeleportSuccess(self):
		"""
		cell实体传送成功的回调
		"""
		KBEngine.globalData["RoomMgr"].TeleportSuccess(self)

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
		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()

	def onTimer(self, TimeId, UserArg):
		if UserArg is 0:
			KBEngine.globalData["RoomMgr"].LeaveRoom(self)

	def onLoseCell(self):
		DEBUG_MSG("Account[%d] onLoseCell" % self.id)
		self.writeToDB()
		self.destroy()

	def onDestroy(self):
		DEBUG_MSG("Account[%d] onDestroy" % self.id)
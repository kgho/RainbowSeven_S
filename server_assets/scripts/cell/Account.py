# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from CHAT_INFO import TChatInfo
import time

class Account(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		#添加定时器(第一次延迟时间20分钟后，循环延迟时间0不循环，传给延迟方法的参数）
		#self.addTimer(20,0,0)

	def Say(self, Msg):
	#被客户端调用的说话方法
		DEBUG_MSG("Account[%i] Say %s" % (self.id, Msg))
		Props = {"Name" : "User" + str(self.id), "Time" : time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()), "Msg" : Msg}
		ChatInfo = TChatInfo().createFromDict(Props)
		self.allClients.OnSay(ChatInfo)

	def onTimer(self, tid, userArg):
		"""
		:param tid:计时器ID
		:param userArg:自定义数据
		"""
		#日志打印
		DEBUG_MSG("Account[%i] onTimer %i" % (self.id, userArg))
		if userArg is 0:
			#销毁这个cell实体，但不会销毁base实体
			self.destroy()
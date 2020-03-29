# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from CHAT_INFO import TChatInfo
import time

class Consumer(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)

	def Say(self, Msg):
	#被客户端调用的说话方法
		DEBUG_MSG("Account[%i] Say %s" % (self.id, Msg))
		Props = {"Name" : self.__ACCOUNT_NAME__, "Time" : time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()), "Msg" : BackMsg}
		ChatInfo = TChatInfo().createFromDict(Props)
		self.allClients.OnSay(ChatInfo)
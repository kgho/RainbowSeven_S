import KBEngine
from KBEDebug import *

class SRoom(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)
		KBEngine.globalData["FirstRoom"] = self

	def onGetCell(self):
		"""
		cell部分被创建成功后的回调函数
		"""
		pass

	def OnLoseCell(self):
		"""
		cell被销毁的回调函数
		"""
		pass
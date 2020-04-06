import KBEngine
from KBEDebug import *

class ERoom(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)

	def GetScriptName(self):
		"""
		获取类名
		:return： 返回类名
		"""
		return self.__class__.__name__

	def onDestroy(self):
		self.destroySpace()
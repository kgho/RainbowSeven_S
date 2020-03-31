import KBEngine
from KBEDebug import *

class SRoom(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)

		self.EntityDict = {}

	def Enter(self, EntityCall):
		"""
		实体进入房间
		：param EntityCall
		"""
		EntityCall.createCallEntity(self.cell)
		self.EntityDict[EntityCall.id] = EntityCall

	def Leave(self, EntityId):
		"""
		实体离开房间
		：param EntityId
		"""
		EntityCall = self.EntityDict[EntityId]
		if EntityCall is None:
			DEBUG_MSG("SRoom %s has no Entity %i" % (self.Name, Entity))
			return

		if EntityCall.cell is not None:
			EntityCall.destroyCellEntity


	def onGetCell(self):
		"""
		cell部分被创建成功后的回调函数
		"""
		KBEngine.globalData["RoomMgr"].OnRoomGetCell(self)

	def OnLoseCell(self):
		"""
		cell被销毁的回调函数
		"""
		KBEngine.globalData["RoomMgr"].OnRoomLoseCell(self.Name)
import KBEngine
from KBEDebug import *
import Math #KBE Vector的包

class SRoom(KBEngine.Space):
	def __init__(self):
		# RoomMgr 创建了两个房间，他们的ID不一样，对应的Cell注册的地图
		if self.base.id % 2 is 1:
			KBEngine.addSpaceGeometryMapping(self.spaceID, None, "spaces/GameMap")
		else:
			KBEngine.addSpaceGeometryMapping(self.spaceID, None, "spaces/TeamMap")

		#创建传送门
		KBEngine.createEntity("Gate", self.spaceID, Math.Vector3(0,0,0), Math.Vector3(0,0,0), {})

	def GetScriptName(self):
		"""
		获取类名
		:return： 返回类名
		"""
		return self.__class__.__name__
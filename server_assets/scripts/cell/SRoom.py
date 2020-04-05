import KBEngine
from KBEDebug import *
import Math #KBE Vector的包

class SRoom(KBEngine.Space):
	def __init__(self):
		KBEngine.addSpaceGeometryMapping(self.spaceID, None, "spaces/GameMap")

		#创建传送门
		KBEngine.createEntity("Gate", self.spaceID, Math.Vector3(0,0,0), Math.Vector3(0,0,0), {})
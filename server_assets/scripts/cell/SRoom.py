import KBEngine
from KBEDebug import *

class SRoom(KBEngine.Space):
	def __init__(self):
		KBEngine.addSpaceGeometryMapping(self.spaceID, None, "spaces/GameMap")
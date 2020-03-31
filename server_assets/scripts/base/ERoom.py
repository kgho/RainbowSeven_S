import KBEngine
from KBEDebug import *

class ERoom(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		self.createCellEntityInNewSpace(None)
		KBEngine.globalData["FirstRoom"] = self
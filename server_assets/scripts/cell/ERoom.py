import KBEngine
from KBEDebug import *

class ERoom(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)

	def onDestroy(self):
		self.destroySpace()
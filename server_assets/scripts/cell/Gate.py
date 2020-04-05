import KBEngine
from KBEDebug import *

class Gate(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)

		self.ControllerId = -1

		#开启定时器，在定时器回调函数中生成触发器（目前这个版本的KBE需要这么做才能保证成功创建触发器）
		#第二个参数为  0  ，不循环的触发器
		self.addTimer(0,0,1)

		#60秒后执行一次的定时器，参数为 2
		#60秒后销毁触发器
		self.addTimer(60, 0, 2)

	def onTimer(self, tid, userArg):
		"""
		定时器回调函数
		:param tid
		:param userArg
		"""
		if userArg is 1:
			DEBUG_MSG("Gate[%d]::addProximity" % self.id)
			#水平方向为3的正方形 对应UE中的长度为300
			self.ControllerId = self.addProximity(3, 0, 0)
		elif userArg is 2:
			DEBUG_MSG("Gate[%d]::cancelController" % self.id)
			self.cancelController(self.ControllerId)

	def onEnterTrap( self, entityEntering, rangeXZ, rangeY, controllerID, userArg = 0 ):
		DEBUG_MSG("Gate[%d]::onEnterTarp entityEntering[%d]" %(self.id, entityEntering.id))


	def onLeaveTrap( self, entityLeaving, rangeXZ, rangeY, controllerID, userArg = 0 ):
		DEBUG_MSG("Gate[%d]::onLeaveTrap entityEntering[%d]" %(self.id, entityLeaving.id))
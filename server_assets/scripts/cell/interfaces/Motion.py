# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class Motion:
    """
    服务端角色移动逻辑接口类
    """
    def __init__(self):
        pass

    def AnimUpdate(self, AnimInfo):
        """
        客户端调用更新动作参数
        :param AnimInfo: 动作参数
        """
        self.otherClients.OnAnimUpdate(AnimInfo)
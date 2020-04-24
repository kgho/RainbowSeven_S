# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import random
import Math

class Role(KBEngine.Proxy):
    def __init__(self):
        KBEngine.Proxy.__init__(self)

        # 保存账户实体
        self.AccountEntity = None

        # 生成初始化位置
        SymbolX = random.randint(0, 1)
        if SymbolX is 0:
            SymbolX = -1
        SymbolY = random.randint(0, 1)
        if SymbolY is 0:
            SymbolY = -1
        #cellData cell实体还没生成的时候给他准备数据
        self.cellData["SpawnPoint"] = Math.Vector3(random.randint(2500, 5000) * SymbolX, random.randint(2500, 5000) * SymbolY, 10)
        DEBUG_MSG("Role[%i] Base __init__. SpawnPoint:%s" % (self.id, self.cellData["SpawnPoint"]))
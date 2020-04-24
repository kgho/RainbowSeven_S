# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class Account(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        ERROR_MSG("Account.Cell::__init__. self.spaceID: %i" % self.spaceID )
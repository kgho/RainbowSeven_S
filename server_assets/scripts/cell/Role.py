# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from interfaces.Character import Character
from interfaces.Motion import Motion

class Role(KBEngine.Entity,
            Character,
            Motion
            ):

    def __init__(self):
        KBEngine.Entity.__init__(self)
        Character.__init__(self)
        Motion.__init__(self)
        ERROR_MSG("Role.Cell::__init__. self.spaceID: %i" % self.spaceID )
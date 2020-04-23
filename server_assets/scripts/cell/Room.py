# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class Room(KBEngine.Space):
    """
    Room的cell部分
    """
    def __init__(self):
        KBEngine.Space.__init__(self)

        ERROR_MSG("Room.Cell::__init__.")
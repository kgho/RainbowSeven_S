# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class Room(KBEngine.Space):
    """
    Room的base部分
    注意：它不是一个实体，并不是真正的space
    真的的space存在于cellapp内存中
    通过这个实体与之关联并操纵space
    """
    def __init__(self):
        KBEngine.Space.__init__(self)

        # 玩家字典， key 实体ID ， value base实体 ，cell实体不考虑
        self.EntityDict = {}

    def Enter(self, EntityRole):
        """
        # 进入房间
        # EntityRole : 进入房间的Entity 的 Base 实体
        """
        # 把实体放入房间的cell空间，调用 self.cell.OnEnter(EntityRole) 也可
        EntityRole.crateCellEntity(self.cell)
        # 将进入的实体保存到玩家字典
        self.EntityDict[EntityRole.id] = EntityRole

    def Leave(self, EntityId):
        """
        # 离开房间(Base实体离开)，如果存在cell实体，也要删除
        """
        # 获取玩家
        EntityRole = self.EntityDict[EntityId]
        # 把玩家移除字典
        del self.EntityDict[EntityId]
        # 销毁玩家cell实体
        # 如果base实体不为空
        if EntityRole is not None:
            # 如果cell实体不为空
            if EntityRole.cell is not None:
                #通过base 实体调用方法 销毁 cell 实体 (销毁后回调该实体的 OnLose方法)
                EntityRole.destroyCellEntity()

    def onGetCell(self):
        """
        # Room 的cell 部分创建成功回调
        """
        # 通知RoomMgr，房间创建成功,self是参数，Room的实体
        KBEngine.globalData["RoomMgr"].OnRoomGetCell(self)

    def onLoseCell(self):
        """
        # Room 的cell 部分销毁成功回调
        """
        # 通知RoomMgr，房间销毁
        KBEngine.globalData["RoomMgr"].OnRoomGetCell(self)
        # 销毁cell实体，同时销毁base实体？
        # self.destroy()
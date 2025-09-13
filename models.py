from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)

    inventory = relationship('Inventory', back_populates='user')
    quests = relationship('UserQuest', back_populates='user')

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)

    inventories = relationship('Inventory', back_populates='item')

class Inventory(Base):
    __tablename__ = 'inventory'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    quantity = Column(Integer, default=1)

    user = relationship('User', back_populates='inventory')
    item = relationship('Item', back_populates='inventories')

class Quest(Base):
    __tablename__ = 'quests'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    xp_reward = Column(Integer, default=0)

    user_quests = relationship('UserQuest', back_populates='quest')

class UserQuest(Base):
    __tablename__ = 'user_quests'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    quest_id = Column(Integer, ForeignKey('quests.id'), primary_key=True)
    status = Column(String, default='in_progress')
    progress = Column(Integer, default=0)

    user = relationship('User', back_populates='quests')
    quest = relationship('Quest', back_populates='user_quests')
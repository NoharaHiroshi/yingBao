# coding=utf-8

from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, Float
from model.base import Base, IdGenerator


class Visit(Base):
    __tablename__ = 'visit'

    TYPE_SECRET, TYPE_TIME = range(2)

    id = Column(BigInteger, default=IdGenerator.gen, primary_key=True)
    ip = Column(String(45), index=True)
    type = Column(Integer, index=True, default=TYPE_SECRET)
    user_agent = Column(String(200))
# coding=utf-8

from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, Float
from model.base import Base, IdGenerator


class Comic(Base):
    __tablename__ = 'comic'

    DELETED, NORMAL = range(2)

    id = Column(BigInteger, default=IdGenerator.gen, primary_key=True)
    name = Column(String(100), index=True, nullable=True)
    state = Column(Integer, default=NORMAL)


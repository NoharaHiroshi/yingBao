# coding=utf-8

from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, Float
from model.base import Base, IdGenerator


class ComicReadRecord(Base):
    __tablename__ = 'comic_read_record'

    id = Column(BigInteger, default=IdGenerator.gen, primary_key=True)
    comic_id = Column(BigInteger, index=True, nullable=True)
    chapter_id = Column(String(100), index=True, nullable=True)
    page = Column(BigInteger, index=True, default=0)

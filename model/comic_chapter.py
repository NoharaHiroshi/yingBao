# coding=utf-8

from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, Float
from model.base import Base, IdGenerator


class ComicChapter(Base):
    __tablename__ = 'comic_chapter'

    id = Column(BigInteger, default=IdGenerator.gen, primary_key=True)
    comic_id = Column(BigInteger, index=True, nullable=True)
    chapter_name = Column(String(100), index=True, nullable=True)
    page_num = Column(BigInteger, index=True, default=0)
    index = Column(BigInteger, index=True, nullable=True)

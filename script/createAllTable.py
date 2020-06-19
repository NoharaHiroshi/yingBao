# coding=utf-8

from model.config.session import engine
from model.base import Base
import model.visit
import model.comic
import model.comic_chapter
import model.comic_read_record


def create_all_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_all_tables()

# coding=utf-8

from model.config.session import engine
from model.base import Base
import model.visit


def create_all_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_all_tables()

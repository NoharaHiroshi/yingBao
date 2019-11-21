# coding=utf-8

import os
import socket
import threading
import datetime
import time
from sqlalchemy import Column, DateTime, text
from sqlalchemy.ext.declarative import declarative_base


class IdGenerator(object):
    _inc = 0
    _inc_lock = threading.Lock()

    @staticmethod
    def gen():
        # 32位时间戳
        new_id = (int(time.time()) & 0xffffffff) << 32
        new_id |= (os.getpid() & 0xff) << 16
        # 16位自增数
        IdGenerator._inc_lock.acquire()
        new_id |= IdGenerator._inc
        IdGenerator._inc = (IdGenerator._inc + 1) & 0xffff
        IdGenerator._inc_lock.release()
        return new_id


class TBase(object):
    created_date = Column(DateTime, default=datetime.datetime.now)
    modified_date = Column(DateTime, default=datetime.datetime.now, onupdate=text('current_timestamp'))


Base = declarative_base(cls=TBase)


if __name__ == '__main__':
    for i in range(0, 100):
        print IdGenerator.gen()
# coding=utf-8

"""开发环境使用的配置
"""

DB_DEBUG = False
DB = 'yin_bao'
HOST = '59.110.226.159'
USER = 'lands'
PASSWORD = '19930203'
CONNECT_STRING = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (USER, PASSWORD, HOST, DB)

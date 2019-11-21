# coding=utf-8
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.config import developer as config

engine = create_engine(
    config.CONNECT_STRING,
    echo=config.DB_DEBUG,
    pool_recycle=3600,
    pool_size=5
)

Session = sessionmaker(bind=engine, autocommit=True)


@contextlib.contextmanager
def get_session(auto_commit=False):
    """
    session 的 contextmanager， 用在with语句
    """
    session = Session(autocommit=auto_commit)
    try:
        yield session
    except Exception as e:
        session.rollback()
        print 'CANT GET SESSION, ERROR: '
        print e
        raise
    finally:
        session.close()

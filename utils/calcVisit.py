# coding=utf-8

from model.config.session import *
from model.visit import *


def calc_visit_count(ip, t, user_agent):
    visit = Visit()
    visit.ip = ip
    visit.type = t
    visit.user_agent = user_agent
    with get_session() as db_session:
        db_session.add(visit)
        db_session.commit()

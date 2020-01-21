# encoding=utf-8

import os
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, session
from script.image2Text import handle_image
from utils.calcVisit import *

website = Blueprint('website', __name__, static_folder='templates')


@website.route('/')
def index():
    calc_visit_count(request.remote_addr, Visit.TYPE_SECRET, request.headers.get("User-Agent"))
    love_num = handle_image()
    context = {
        'love_num': love_num
    }
    return render_template('index.html', **context)


@website.route('/time')
def time():
    calc_visit_count(request.remote_addr, Visit.TYPE_TIME, request.headers.get("User-Agent"))
    context = {
        'time': ""
    }
    return render_template("time.html", **context)


@website.route('/card')
def card():
    calc_visit_count(request.remote_addr, Visit.TYPE_CARD, request.headers.get("User-Agent"))
    context = {
        'card': ""
    }
    return render_template("YinBaoAlbum.html", **context)


if __name__ == "__main__":
    print os.path.dirname(__file__)
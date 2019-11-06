# encoding=utf-8

import os
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, session
from script.image2Text import handle_image

website = Blueprint('website', __name__, static_folder='templates')


@website.route('/')
def index():
    love_num = handle_image()
    context = {
        'love_num': love_num
    }
    return render_template('index.html', **context)


@website.route('/time')
def time():
    context = {
        'time': ""
    }
    return render_template("time.html", **context)


if __name__ == "__main__":
    print os.path.dirname(__file__)
# encoding=utf-8

import os
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, session
from script.image2Text import handle_image
from model.comic import *
from model.comic_chapter import *
from model.comic_read_record import *
from model.config.session import *
from utils.calcVisit import *

website = Blueprint('website', __name__, static_folder='templates')


@website.route('/index')
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


@website.route("/comic_list")
def comic_list():
    comic_list_info = list()
    context = {
        "comic_list": comic_list_info
    }
    with get_session() as db_session:
        comics = db_session.query(Comic).all()
        for comic in comics:
            comic_info = {
                "id": str(comic.id),
                "name": comic.name
            }
            comic_list_info.append(comic_info)
    return render_template("comic_index.html", **context)


@website.route("/comic_chapter_list")
def chapter_list():
    comic_id = request.args.get('comic_id')
    chapter_list_info = list()
    context = {
        "name": '',
        "comic_id": comic_id,
        "chapter_list": chapter_list_info
    }
    with get_session() as db_session:
        comic = db_session.query(Comic).get(comic_id)
        chapter_data = db_session.query(ComicChapter).filter(
            ComicChapter.comic_id == comic_id
        ).order_by(ComicChapter.index).all()
        for chapter in chapter_data:
            chapter_info = {
                "id": chapter.id,
                "name": chapter.chapter_name,
                "index": chapter.index
            }
            chapter_list_info.append(chapter_info)
    context["name"] = comic.name
    return render_template("comic_chapter_index.html", **context)


@website.route("/comic_chapter_content")
def comic_chapter_content():
    comic_id = request.args.get('comic_id')
    chapter_id = request.args.get('chapter_id')
    img_url_list = list()
    context = {
        "comic_name": "",
        "chapter_name": "",
        "chapter_page": 0,
        "img_url_list": img_url_list
    }
    with get_session() as db_session:
        comic = db_session.query(Comic).get(comic_id)
        chapter = db_session.query(ComicChapter).get(chapter_id)
    comic_base_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"), "comic")
    comic_path = os.path.join(comic_base_path, comic.name)
    chapter_name = "%s_%s" % (chapter.index, chapter.chapter_name)
    comic_chapter_path = os.path.join(comic_path, chapter_name)
    img_file_list = os.walk(comic_chapter_path)
    for root, dirs, files in img_file_list:
        for f in files:
            url = "/static/comic/%s/%s/%s" % (comic.name, chapter_name, f)
            url = url.replace(" ", "%20")
            img_url_list.append(url)
    context.update({
        "comic_name": comic.name,
        "chapter_name": chapter.chapter_name,
        "chapter_page": chapter.page_num,
        "img_url_list": img_url_list
    })
    return render_template("comic_chapter_content.html", **context)

# @website.route("/comic_chapter_content")
# def comic_chapter():
#     chapter_id = request.args.get('chapter_id')
#     comic_id = request.args.get('comic_id')
#     page = request.args.get("page")
#     with get_session() as db_session:
#
#         # comic_read_record = db_session.query(ComicReadRecord).filter(
#         #     ComicReadRecord.comic_id == comic_id
#         # ).first()
#         # if not comic_read_record:
#         #     comic_read_record = ComicReadRecord()
#         #     comic_read_record.comic_id = comic_id
#         #     comic_read_record.chapter_id = chapter_id
#
#
#     return render_template("comic_chapter_index.html", **context)

if __name__ == "__main__":
    print os.path.dirname(__file__)
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
                "name": comic.name,
                "cover": "/static/comic_cover/%s.jpg" % comic.name
            }
            comic_list_info.append(comic_info)
    return render_template("comic_index.html", **context)


@website.route("/comic_chapter_list")
def chapter_list():
    comic_id = request.args.get('comic_id')
    chapter_list_info = list()
    context = {
        "name": '',
        "comic_id": str(comic_id),
        "chapter_list": chapter_list_info,
        "continue_chapter_id": "",
        "continue_chapter_name": "",
        "continue_page": 0
    }
    with get_session() as db_session:
        comic = db_session.query(Comic).get(comic_id)
        chapter_data = db_session.query(ComicChapter).filter(
            ComicChapter.comic_id == comic_id
        ).order_by(-ComicChapter.index).all()
        comic_read_record = db_session.query(ComicReadRecord).filter(
            ComicReadRecord.comic_id == comic_id
        ).first()
        if comic_read_record:
            chapter_record = db_session.query(ComicChapter).get(comic_read_record.chapter_id)
            context["continue_chapter_id"] = str(comic_read_record.chapter_id)
            context["continue_chapter_name"] = chapter_record.chapter_name
            context["continue_page"] = comic_read_record.page
        for chapter in chapter_data:
            chapter_info = {
                "id": str(chapter.id),
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
        "img_url_list": img_url_list,
        "comic_id": str(comic_id),
        "chapter_id": str(chapter_id),
        "page_num": "",
        "next_chapter_id": "",
        "before_chapter_id": ""
    }
    with get_session() as db_session:
        comic = db_session.query(Comic).get(comic_id)
        chapter = db_session.query(ComicChapter).get(chapter_id)
        next_chapter = db_session.query(ComicChapter).filter(
            ComicChapter.comic_id == comic_id,
            ComicChapter.index == chapter.index + 1
        ).first()
        before_chapter = db_session.query(ComicChapter).filter(
            ComicChapter.comic_id == comic_id,
            ComicChapter.index == chapter.index - 1
        ).first()
    comic_base_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"), "comic")
    comic_path = os.path.join(comic_base_path, comic.name)
    chapter_name = "%s_%s" % (chapter.index, chapter.chapter_name)
    comic_chapter_path = os.path.join(comic_path, chapter_name)
    img_file_list = os.walk(comic_chapter_path)
    for root, dirs, files in img_file_list:
        for i in range(len(files)):
            f = files[i]
            url = "/static/comic/%s/%s/%s" % (comic.name, chapter_name, f)
            url = url.replace(" ", "%20")
            img_url_list.append({
                "url": url,
                "file": f
            })
    img_url_list.sort(key=lambda x: int(x["file"].split(".")[0]))
    for i in range(len(img_url_list)):
        img_url_list[i]["id"] = i
    context.update({
        "comic_name": comic.name,
        "chapter_name": chapter.chapter_name,
        "chapter_page": chapter.page_num,
        "img_url_list": img_url_list,
        "page_num": len(img_url_list),
        "next_chapter_id": str(next_chapter.id),
        "before_chapter_id": str(before_chapter.id)
    })
    return render_template("comic_chapter_content.html", **context)


@website.route("/comic_read_record", methods=['POST'])
def comic_chapter():
    result = {
        "response": "success",
        "info": ""
    }
    chapter_id = request.form.get('chapter_id')
    comic_id = request.form.get('comic_id')
    page = request.form.get("page")
    with get_session() as db_session:

        comic_read_record = db_session.query(ComicReadRecord).filter(
            ComicReadRecord.comic_id == comic_id
        ).first()
        if not comic_read_record:
            comic_read_record = ComicReadRecord()
            comic_read_record.comic_id = comic_id
            comic_read_record.chapter_id = chapter_id
            comic_read_record.page = page
            db_session.add(comic_read_record)
        else:
            comic_read_record.chapter_id = chapter_id
            comic_read_record.page = page
        db_session.commit()
    return jsonify(result)


if __name__ == "__main__":
    print os.path.dirname(__file__)
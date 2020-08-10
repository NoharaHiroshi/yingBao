# encoding=utf-8

import os
from model.config.session import *
from model.comic_chapter import *
from model.comic import *
from model.base import *

COMIC_PATH = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"), "comic")


def scan_comic(comic_path=COMIC_PATH):
    with get_session() as db_session:
        for comic_name in os.listdir(comic_path):
            comic_name_path = os.path.join(comic_path, comic_name)
            comic_data = db_session.query(Comic).filter(
                Comic.name == comic_name
            ).first()
            if not comic_data:
                comic_id = IdGenerator.gen()
                comic_data = Comic()
                comic_data.id = comic_id
                comic_data.name = comic_name
                db_session.add(comic_data)

                chapter_files = os.listdir(comic_name_path)
                for chapter_name in chapter_files:
                    chapter_file_path = os.path.join(comic_name_path, chapter_name)
                    img_files = os.listdir(chapter_file_path)
                    index = chapter_name.split("_")[0]
                    title = "_".join(chapter_name.split("_")[1:])
                    chapter = ComicChapter()
                    chapter.index = index
                    chapter.chapter_name = title
                    chapter.comic_id = comic_id
                    chapter.page_num = len(img_files)
                    db_session.add(chapter)
        db_session.commit()


if __name__ == "__main__":
    path = u""
    scan_comic(path)

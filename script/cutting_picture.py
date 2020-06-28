# encoding=utf-8

import os
import random
from PIL import Image


def convert_img(file_path):
    dst_path = os.path.join(os.path.split(file_path)[0], "%s_convert" % os.path.split(file_path)[1])
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    for root, dirs, files in os.walk(file_path):
        for i in range(len(files)):
            name = files[i]
            print "convert_img: %s" % name
            img_path = os.path.join(root, name)
            new_img_path = os.path.join(dst_path, "%s.jpg" % name.split(".")[0])
            img = Image.open(img_path)
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img)
            bg.save(new_img_path)
    return dst_path


def cutting_image(file_path):
    dst_path = os.path.join(os.path.split(file_path)[0], "%s_cutting" % os.path.split(file_path)[1])
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    for root, dirs, files in os.walk(file_path):
        files.sort(key=lambda x: int(x.split(".")[0]))
        for i in range(len(files)):
            name = files[i]
            print "cutting_image: %s" % name
            img_path = os.path.join(root, name)
            img = Image.open(img_path)
            if len(img.split()) == 4:
                r, g, b, a = img.split()
                img = Image.merge("RGB", (r, g, b))
            w, h = img.size
            new_w = w // 2
            for r in range(2):
                box = (r * new_w, 0, (r + 1) * new_w, h)
                new_name = "%s.jpg" % (2 * i + 1 if r == 0 else 2 * i)
                img.crop(box).save(os.path.join(dst_path, new_name))


if __name__ == "__main__":
    path = u"D:\\myWork\\downloadComics\\杀戮都市GANTZ\\7_第8卷"
    # dst_path = convert_img(path)
    cutting_image(path)
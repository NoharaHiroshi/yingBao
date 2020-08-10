# encoding=utf-8

import os
import re
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
    img_dict = dict()
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    for root, dirs, files in os.walk(file_path):
        # files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
        files.sort(key=lambda x: int(re.search("\d+", x).group()) if re.search("\d+", x) else 9999)
        for name in files:
            img_path = os.path.join(root, name)
            img = Image.open(img_path)
            w, h = img.size
            if w not in img_dict:
                img_dict[w] = 1
            else:
                img_dict[w] += 1
        print u"图片尺寸分析：%s" % img_dict
        w_list = sorted(img_dict.items(), key=lambda x: x[1], reverse=True)
        max_w = w_list[0][0]
        print u"标准图片大小：%s" % max_w
        page_num = 1
        for i in range(len(files)):
            try:
                name = files[i]
                img_format = name.split(".")[-1]
                img_path = os.path.join(root, name)
                img = Image.open(img_path)
                w, h = img.size
                if w != max_w and w < max_w * 0.9:
                    new_w = w
                    box = (0, 0, new_w, h)
                    new_name = "%s.%s" % (page_num, img_format)
                    img.crop(box).save(os.path.join(dst_path, new_name))
                    page_num += 1
                else:
                    new_w = w // 2
                    for r in range(2):
                        box = (r * new_w, 0, (r + 1) * new_w, h)
                        if r == 0:
                            new_name = "%s.%s" % (page_num+1, img_format)
                        else:
                            new_name = "%s.%s" % (page_num, img_format)
                        img.crop(box).save(os.path.join(dst_path, new_name))
                    page_num += 2
            except Exception as e:
                print e
                continue


def change_file_name(file_path):
    for root, dirs, files in os.walk(file_path):
        for dir in dirs:
            os.rename(os.path.join(root, dir), os.path.join(root, dir.replace("_cutting", "")))


if __name__ == "__main__":
    file_path = u""
    # for root, dirs, files in os.walk(file_path):
    #     for dir in dirs:
    #         file_path = os.path.join(root, dir)
    #         print file_path
    #         cutting_image(file_path)
    change_file_name(file_path)
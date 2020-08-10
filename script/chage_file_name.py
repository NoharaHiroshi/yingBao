# encoding=utf-8

import os
import re


def change_chapter_name(file_path):
    for root, dirs, files in os.walk(file_path):
        dirs.sort(key=lambda x: int(re.search("\d+", x).group()) if re.search("\d+", x) else 9999)
        for i in range(len(dirs)):
            dir = dirs[i]
            new_dir = "%s_Vol.%s" % (i, i+1)
            print dir, new_dir
            os.rename(os.path.join(root, dir), os.path.join(root, new_dir))


def change_img_name(file_path):
    for root, dirs, files in os.walk(file_path):
        dirs.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
        print dirs
        for i in range(len(files)):
            name = os.path.join(root, files[i])
            img_format = name.split(".")[-1]
            _name = "%s.%s" % (i, img_format)
            new_name = os.path.join(root, _name)
            print "name: %s | new_name: %s" % (name, new_name)
            os.rename(name, new_name)


if __name__ == "__main__":
    path = u""
    change_chapter_name(path)
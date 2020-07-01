# encoding=utf-8

import os
import re


def change_chapter_name(file_path):
    for root, dirs, files in os.walk(file_path):
        # dirs.sort(key=lambda x: int(re.search("\d+", x).group()) if re.search("\d+", x) else 9999)
        for i in range(len(dirs)):
            dir = dirs[i]
            # new_dir = re.search("Vol_\d+", dir).group()
            new_dir = dir.replace("_cutting", "")
            print dirs[i], new_dir
            os.rename(os.path.join(root, dir), os.path.join(root, new_dir))
        # for i in range(len(files)):
        #     name = files[i]
        #     print "name: %s" % name


def change_img_name(file_path):
    for root, dirs, files in os.walk(file_path):
        print root
        for i in range(len(files)):
            name = os.path.join(root, files[i])
            _name = files[i].split("_")[-1]
            new_name = os.path.join(root, "%s_%s" % (i, _name))
            print "name: %s | new_name: %s" % (name, new_name)
            os.rename(name, new_name)


if __name__ == "__main__":
    path = u"F:\downloads\全职猎人"
    change_chapter_name(path)
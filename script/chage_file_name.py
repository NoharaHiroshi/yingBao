# encoding=utf-8

import os
import re


def change_chapter_name(file_path):
    for root, dirs, files in os.walk(file_path):
        dirs.sort(key=lambda x: int(re.search("\d+", x).group()) if re.search("\d+", x) else 9999)
        for i in range(len(dirs)):
            dir = dirs[i]
            print dirs[i]
            os.rename(os.path.join(root, dir), os.path.join(root, "%s_%s" % (i, dir)))
        # for i in range(len(files)):
        #     name = files[i]
        #     print "name: %s" % name


def change_img_name(file_path):
    for root, dirs, files in os.walk(file_path):
        print root
        for i in range(len(files)):
            name = os.path.join(root, files[i])
            _name = files[i].replace("圣斗士星矢冥王神话NEXT DIMENSION_")
            new_name = os.path.join(root, "%s_%s" % (i, _name))
            print "name: %s | new_name: %s" % (name, new_name)
            # os.rename(name, os.path.join(root, "%s_%s" % (i, files[i])))


if __name__ == "__main__":
    path = u"D:\myWork\love\yingBao\static\comic\圣斗士冥王神话ND"
    change_chapter_name(path)
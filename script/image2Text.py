# encoding=utf-8

import os
import random
from PIL import Image

IMG = os.path.join(os.path.dirname(__file__), "love.jpg")

WIDTH = 80
HEIGHT = 20

# 记录生日 0203
ascii_char = ["023", "1456789"]


def get_char(r, g, b, alpha=256):  # alpha透明度
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)  # 计算灰度
    unit = (256.0 + 1) / length
    t = ascii_char[int(gray / unit)]
    return random.choice(t)


def handle_image():
    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
    txt = ""
    for i in range(HEIGHT):
        txt += "<p>"
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j, i)))
        txt += "</p>"
    return txt


if __name__ == "__main__":
    print handle_image()


# coding=utf-8

import datetime
import os
import fitz


def pyMuPDF_fitz(pdfPath, imagePath):
    print("imagePath=" + imagePath)
    pdf_doc = fitz.open(pdfPath)
    for pg in range(pdf_doc.pageCount):
        print "%s.png" % str(pg)
        page = pdf_doc[pg]
        rotate = int(0)
        zoom_x = 1
        zoom_y = 1
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.writePNG(imagePath + '/' + '%s.png' % pg)  # 将图片写入指定的文件夹内


if __name__ == "__main__":
    pdfPath = u'F:\BaiduNetdiskDownload\【蜡笔小新】·第30卷.pdf'
    imagePath = u'F:\BaiduNetdiskDownload\蜡笔小新 第30卷'
    pyMuPDF_fitz(pdfPath, imagePath)
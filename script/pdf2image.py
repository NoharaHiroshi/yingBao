# coding=utf-8

import datetime
import os
import fitz
import glob


def pdf2pic(pdfPath, imagePath):
    print("imagePath=" + imagePath)
    pdf_doc = fitz.open(pdfPath)
    for pg in range(pdf_doc.pageCount):
        print "%s.jpg" % str(pg)
        page = pdf_doc[pg]
        rotate = int(0)
        zoom_x = 2
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.writePNG(imagePath + '/' + '%s.jpg' % pg)  # 将图片写入指定的文件夹内


def pic2pdf(image_path, pdf_path):
    doc = fitz.open()
    for root, dirs, files in os.walk(image_path):
        files.sort(key=lambda x: int(x.split(".")[0]))
        print files
        for i in range(len(files)):
            img = os.path.join(root, files[i])
            imgdoc = fitz.open(img)         # 打开图片
            pdfbytes = imgdoc.convertToPDF()    # 使用图片创建单页的 PDF
            imgpdf = fitz.open("pdf", pdfbytes)
            doc.insertPDF(imgpdf)          # 将当前页插入文档
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    doc.save(pdf_path)          # 保存pdf文件
    doc.close()


if __name__ == "__main__":
    # pdfPath = u'E:\\扫描\\2020-08-13_154502.pdf'
    # imagePath = u'E:\\扫描\\反面'
    # pyMuPDF_fitz(pdfPath, imagePath)
    pic2pdf()
#!/usr/bin/env python
#coding:utf-8

import os
import sys

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal

reload(sys)
sys.setdefaultencoding("utf-8")



from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice



from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

def get_content(document):
    # Get the outlines of the document.
    try:
        outlines = document.get_outlines()
        for (level,title,dest,a,se) in outlines:
            print (level, title)
    except:
        raise PDFNoOutlines
        pass


def get_skip_page(page_num,skip_page_num):

    for skip_num in skip_page_num:
        if skip_num == page_num:
            return True

    return False


if __name__ == '__main__':

    fp = open('data/sta_industry_data.pdf', 'rb')
    # 创建一个PDF文档解析器对象
    parser = PDFParser(fp)
    # 创建一个PDF文档对象存储文档结构
    # 提供密码初始化，没有就不用传该参数
    # document = PDFDocument(parser, password)
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # 获取文件提纲
    # get_content(document)

    # 设定参数进行分析
    laparams = LAParams()
    # 创建一个PDF资源管理器对象来存储共享资源
    rsrcmgr = PDFResourceManager()

    # 创建一个pdf设备对象
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解析器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    skip_page_num = (1,100)
    page_count = 1
    # 处理每一页
    for page in PDFPage.create_pages(document):

        interpreter.process_page(page)

        # if get_skip_page(page_count,skip_page_num):
        #     continue

        # 接受该页面的LTPage对象
        layout = device.get_result()
        for x in layout:
            if (isinstance(x, LTTextBoxHorizontal)):
                with open('a.txt', 'a') as f:
                    f.write(x.get_text().encode('utf-8') + '\n')


        if page_count > 12:
            break
        page_count += 1



    pass


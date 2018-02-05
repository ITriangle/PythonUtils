#!/usr/bin/env python
# coding:UTF-8

from PIL import Image
import pytesseract

def pytesseract_word(path_image):
    # pip install pytesseract 先安装依赖包


    # lang 指定中文简体
    text = pytesseract.image_to_string(Image.open(path_image), lang='chi_sim')
    print(text)

if __name__ == '__main__':


    image_path = '../data/denggao.jpg'
    # image_path = '/home/wl/WLWork/Tmp_Git/2017-12306-master/screenshots/shot3.png'
    # image_path = '/home/wl/WLWork/Tmp_Git/2017-12306-master/screenshots/captcha-image.jpg'
    pytesseract_word(image_path)
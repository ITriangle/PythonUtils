#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division

import sys
import os
import logging
import ConfigParser
import time
from datetime import datetime, timedelta

reload(sys)
sys.setdefaultencoding("utf-8")


logger = logging.getLogger("python_utils")


"""
公共配置区域函数
"""
# 根目录
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
# 配置目录
CONF_DIR = os.path.join(ROOT_DIR, "conf")
# 基础时间
BASE_TIME=time.strftime("%Y-%m-%d",time.localtime())
# 配置文件路径
CONFIGFILE = os.path.join(CONF_DIR, "config.ini")
DB_SCRIPT_TEMPLATE = os.path.join(CONF_DIR, "db_script_template")
# 存放生成hql脚本目录
DB_SCRIPT_RUNNING = os.path.join(ROOT_DIR,"db_script_running")
if not os.path.exists(DB_SCRIPT_RUNNING):
    os.makedirs(DB_SCRIPT_RUNNING)

# log 目录
LOG_DIR_PATH = os.path.join(ROOT_DIR,'logs')
if not os.path.exists(LOG_DIR_PATH):
    os.makedirs(LOG_DIR_PATH)

'''
获取配置属性的常规函数
'''
# 加载配置文件
def load_conf(conf_path):
    conf_loader = ConfigParser.ConfigParser()
    conf_loader.read(conf_path)

    return conf_loader

# 获取字符串分割的属性
def get_multi(config,key1,key2,delimiter=";"):
    value_array = config.get(key1, key2).split(delimiter)

    return value_array

# 获取单一属性
def get_single(config,key1,key2):
    value_array = config.get(key1, key2)

    return value_array

# 获取 section 下的所有 key
def get_section_all_key(config,section):
    return dict(config.items(section))
    pass

# 获取当前脚本的执行用户
def get_current_user():
    import getpass
    return getpass.getuser()



if __name__ == '__main__':
    # CONFIGFILE = '/home/wl/WLWork/data_integration/python_utils/filter_data/conf/config.ini'

    conf = load_conf(CONFIGFILE)
    db_conf = get_section_all_key(conf,'db')

    for key in db_conf:
        print key,db_conf[key]

    print dict(conf.items('db'))

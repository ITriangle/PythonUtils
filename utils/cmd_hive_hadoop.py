#!/usr/bin/env python
#coding:utf-8

import os
import shlex
import subprocess
import time
import log
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

logger = log.getLogger("python_utils")


def run_hive_script(hql):
    process = subprocess.Popen(shlex.split('''
        hive -f %s
    ''' % (hql)))
    while True:
        return_code = process.poll()
        if return_code is None:
            time.sleep(5)
            continue

        if return_code != 0:
            msg = 'hql:%s run fail' % (hql)
            logger.error(msg)
            return False
        else:
            logger.info('hql:%s done.' % ( hql ))
            return True


def run_hadoop_jar(jar, main, input_p, output):
    command = ''' 
        hadoop jar %s %s %s %s
    ''' % (jar, main, input_p, output)
    process = subprocess.Popen(shlex.split(command))
    while True:
        return_code = process.poll()
        if return_code is None:
            time.sleep(5)
            continue
        if return_code != 0:
            logger.warn('fail task << %s >>...' % (command))
            return False
        else:
            logger.info('success task << %s >>.' % (command))
            return True


# 获取目录下的所有文件
def get_all_file_from_dir(dir_path):
    file_path_list = []
    files = os.listdir(dir_path)
    for file in files:
        file_path = os.path.join(dir_path, file)
        if os.path.isdir(file_path):
            for path in get_all_file_from_dir(file_path):
                file_path_list.append(path)
            continue
        else:
            file_path_list.append(file_path)

    return file_path_list

if __name__ == '__main__':


    pass
#!/usr/bin/env python
# coding=utf-8
import os
import sys

import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler
from logging import Formatter


ROOT_DIR=None
COMMON_SMTP_HOST='smtp_host'
COMMON_SMTP_PORT='smtp_port'
COMMON_FROM='email_username'
COMMON_PASS='email_password'


def log_path(safe_process=True):
    """
    创建日志需要的目录，并返回日志的路径
    :return: 
    """
    every_log_path = os.path.join(ROOT_DIR, "log")
    if not os.path.exists(every_log_path):
        os.makedirs(every_log_path)
    if safe_process is True:
        log_file_path = os.path.join(every_log_path, "{}_log.log".format(os.getpid()))
    else:
        log_file_path = os.path.join(every_log_path, "{}_log.log".format('gaokao_web'))

    return log_file_path


def init_log_mail_handler(app_logger, logger_level=None):
    """
    邮件发送日志，发送的级别为 ERROR
    :param app_logger: 
    :return: 
    """
    SMTP_HOST = COMMON_SMTP_HOST
    SMTP_PORT = COMMON_SMTP_PORT

    FROM = COMMON_FROM
    PASS = COMMON_PASS

    TO = ['wanglong@ipin.com']

    if (logger_level is None) or (logger_level == logging.DEBUG):
        mail_handler = SMTPHandler(
            (SMTP_HOST, SMTP_PORT)
            , FROM
            , TO
            , '[数据Web服务 FAIL]处理过程中存在错误已经捕获,详情查看邮件日志'
            , (FROM, PASS))
        # 设置发送邮件的日志级别
        mail_handler.setLevel(logging.ERROR)
        # 设置邮件日志格式
        mail_handler.setFormatter(Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
        '''))
        app_logger.addHandler(mail_handler)


def init_log_console_handler(app_logger,logFormatter_web):
    """
    输出到控制台
    :param app_logger: 
    :return: 
    """
    consoleHandler_web = logging.StreamHandler()
    consoleHandler_web.setFormatter(logFormatter_web)
    app_logger.addHandler(consoleHandler_web)

def init_log_file_handler(app_logger,logFormatter_web):
    '''写日志文件'''
    fileHandler_web = logging.FileHandler(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                       "log",
                                                       "{}.log".format(datetime.now().isoformat()[:10].replace('-', ''))))
    fileHandler_web.setFormatter(logFormatter_web)
    app_logger.addHandler(fileHandler_web)

def init_log_rotating_file_handler(app_logger,logFormatter_web, logger_level=None):
    """
    写文件到日志，超过设置文件大小，就生成新的文件
    :param app_logger: 
    :return: 
    """
    MAX_BYTES = 10000
    BACKUP_COUNT = 10
    if (logger_level is None) or (logger_level == logging.DEBUG):
        file_handler = RotatingFileHandler(log_path(safe_process=False), maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
        file_handler.setFormatter(logFormatter_web)
        # file_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)
        app_logger.addHandler(file_handler)


def init_log_time_rotating_file_handler(app_logger,logFormatter_web):
    """
    每天凌晨生成一个新的日志文件，
    每一个进程单独的日志文件
    :return: 
    """
    every_day_handler = logging.handlers.TimedRotatingFileHandler(log_path(), 'midnight', 1)
    every_day_handler.setFormatter(logFormatter_web)
    app_logger.addHandler(every_day_handler)


'''日志配置'''
# create Logger and Formatter
logFormatter_web = logging.Formatter(
    '%(asctime)s [%(levelname)s] (%(pathname)s:%(lineno)d@%(funcName)s) -> %(message)s')
rootLogger_web = logging.getLogger("gaokao_data_web")
# rootLogger_web.setLevel(logging.INFO)
rootLogger_web.setLevel(logging.DEBUG)
init_log_time_rotating_file_handler(rootLogger_web,logFormatter_web)
init_log_console_handler(rootLogger_web,logFormatter_web)
init_log_mail_handler(rootLogger_web)

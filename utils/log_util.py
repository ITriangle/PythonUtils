#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division


import sys
import os
import logging


reload(sys)
sys.setdefaultencoding("utf-8")



logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(pathname)s:%(lineno)d@%(funcName)s) -> %(message)s')
rootLogger = logging.getLogger("sync_pg2hive")
rootLogger.setLevel(logging.INFO)
rootLogger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

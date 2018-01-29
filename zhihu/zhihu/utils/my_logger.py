# -*- coding: utf-8 -*-

import logging
import os
import os.path
from datetime import datetime, timedelta

if not os.path.exists('logging_dir'):
    os.mkdir('logging_dir')

def MyLogger():
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        self.handler = logging.FileHandler('logging_dir' + name + '.log')
        self.logger.setLevel(logging.DEBUG)
        self.handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)

    def log(self, msg=''):
        self.logger.debug(msg)
        self.logger.debug(u'时间是%s' % datetime.now().strftime(u'%Y年%m月%d日 %H:%M:%S'))

# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/7/6 16:39 
  @Auth : 于洋
  @File : log.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""

import logging
import os.path
from logging.handlers import TimedRotatingFileHandler

from common.path import log_dir


class Log(logging.Logger):
    """
    日志能力
    """
    def __init__(self, name='日志', level='DEBUG', file=None):
        super().__init__(name, level)
        # 日志格式
        fmt = logging.Formatter("%(levelname)s-%(asctime)s%(filename)s--%(funcName)-s [line:%(lineno)d] : %(message)s")
        # 日志处理器

        p = logging.StreamHandler()
        p.setFormatter(fmt)
        self.addHandler(p)
        # 文件处理器
        if file:
            f = TimedRotatingFileHandler(f'{os.path.join(log_dir,file)}', when='D', backupCount=7, encoding='utf-8')
            f.setFormatter(fmt)
            self.addHandler(f)


if __name__ == '__main__':
    pass
















































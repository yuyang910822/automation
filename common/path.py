# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/7/6 16:13 
  @Auth : 于洋
  @File : path.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""

import os

# 根
dirs = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

mysql_dir = os.path.join(dirs, r'config\mysql.yaml')

log_dir = os.path.join(dirs, r'log')

jd_log_dir = os.path.join(log_dir, r'JD.log')

jd_api_dir = os.path.join(dirs, r'data\jd_api.yaml')

test_dir = os.path.join(dirs, r'testcase')

report_dir = os.path.join(dirs, r'report')

url_dir = os.path.join(dirs, r'data\{}.yaml')

url_config_dir = os.path.join(dirs, r'config\url_config.yaml')

config_ini_dir = os.path.join(dirs, r'config\config.ini')

if __name__ == '__main__':
    print(log_dir + '\\' + '1')

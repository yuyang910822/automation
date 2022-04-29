# -*- coding: utf-8 -*- 
# @Time : 2022/1/20 16:15 
# @Author : Yu yang
# @File : runtiest.py
import os
import time

import jsonpath
import requests
from requests import Response

from common.log import Cluster_log
from common.mysql import Mysql
from common.path import mysql_dir, jd_log_dir, jd_api_dir, dirs, url_dir, url_config_dir
from common.readYaml import readYaml


class Base(Mysql):
    """
    公共方法层,业务层继承基类，方便调用
    """

    def __init__(self, db_name: str, log_name: str, url_file_name: str, host: str):
        """
        基础类
        :param db_name: 数据库名称 ../config/mysql.yaml
        :param log_name: 日志名称 生成日志文件时必传
        :param url_file_name: 接口测试数据文件名称 ../config/****
        :param host: url_file_name环境的host
        """
        super(Base, self).__init__(mysql_data=readYaml(mysql_dir)[db_name], file=log_name)
        self.url = readYaml(url_dir.format(url_file_name))
        # 通过读取host，更新对应请求数据url中的host
        localhost = readYaml(url_config_dir)[host]
        for url in self.url:
            if 'rpm' in self.url[url]['url']:
                self.url[url]['url'] = str(self.url[url]['url']).replace('/rpm/', localhost[0])
            elif 'rcs' in self.url[url]['url']:
                self.url[url]['url'] = str(self.url[url]['url']).replace('/rcs/', localhost[1])
            else:
                self.error(f"未替换：{self.url[url]['url']}")

    # def re(self, loc):
    #     """
    #     通过字典
    #     :param loc: 接口依赖数据：请求方式，请求地址，请求头，请求体
    #     :return:
    #     """
    #     method, url, headers, json = loc
    #     self.log.info(f'接口入参：\n{method}，{url}\n{headers}\n{json}')
    #     r = requests.request(method=method, url=url, headers=headers, json=json)
    #     self.log.info(f'响应体:{r.json()}')
    #     return r

    def re1(self, info: dict) -> Response:
        """
        封装接口请求
        :param 请求信息
        :return: 响应信息
        """
        times = int(time.time() * 1000)
        self.info(f'{info["url"]}--|{times}|>>>>>{info["json"]}')
        r = requests.request(**info)
        self.info(f'{info["url"]}--|{times}|<<<<<{r.json()}')
        return r

    def setProperties(self, name: str) -> int:
        """
        设置属性
        :param name:实例变量名称
        :return: 毫秒时间戳
        """
        t = int(time.time()*1000)
        setattr(self, name, t)
        return t

    def getToken(self, info: dict) -> str:
        """

        登录获取对应token
        :param info: 请求信息
        :return:
        """
        try:
            r = self.re1(info)
            token = jsonpath.jsonpath(r.json(), '$..token')[0]
        except BaseException as e:
            self.error(f'Token获取失败:{r.json()}')
        else:
            return token

    @staticmethod
    def getDate():
        """
        获取日期
        :return:
        """
        return time.strftime("%Y-%m-%d")

    @staticmethod
    def getDateTime():
        """
        获取日期时间
        :return:
        """
        return time.strftime("%Y-%m-%d|%H:%M:%S")

    @staticmethod
    def getTime():
        """
        获取日期时间
        :return:
        """
        return time.strftime("%H%M%S")

    @staticmethod
    def getTimeStamp(self):
        """时间戳"""
        return time.time() * 1000


if __name__ == '__main__':
    f = Base('kk_mysql', '1', 'jd_api', 'kk_prod')
    ff = {"method": "post", "url": "http://10.74.51.251:8010/user-center/user/login",
          "json": {"timeout": 3000, "userName": "jd_admin",
                   "password": "73b515a26358508c672842dedea60763c8be8e00123d35095bb3f3e9c9fa8f44"}}

    print(f.getToken(f.url['login']))

# -*- coding: utf-8 -*- 
# @Time : 2022/1/20 16:15 
# @Author : Yu yang
# @File : runtiest.py
import configparser
import os
import time,datetime

import requests

from requests import Response
from common.mysql import Mysql
from common.path import mysql_dir, url_dir, url_config_dir, config_ini_dir
from common.readYaml import readYaml
from jira_remind.issou import *


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
            elif 'erms' in self.url[url]['url']:
                self.url[url]['url'] = str(self.url[url]['url']).replace('/erms/', localhost[2])
            else:
                self.error(f"未替换：{self.url[url]['url']}")
        self.t = time.mktime(datetime.date.today().timetuple())
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.t - 21600))
        self.endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.t + 64800))

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

    def re1(self, info: dict,tag=1) -> Response:
        """
        封装接口请求
        :param 请求信息
        :return: 响应信息
        """
        times = int(time.time() * 1000)

        if 'forwardx.com' in info['url']:
            info['headers']['token'] = jsonpath.jsonpath(requests.request(**self.url['login']).json(), '$..token')[0]
        self.info(f'{str(info["url"])}--|{times}|>>>>>{info["json"]}')
        r = requests.request(**info)
        self.info(f'{str(info["url"]).split("/")[-1]}--|{times}|<<<<<{r.json()}')
        return r

    def setProperties(self, name: str) -> int:
        """
        设置属性
        :param name:实例变量名称
        :return: 毫秒时间戳
        """
        t = int(time.time() * 1000)
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
        获取时间
        :return:
        """
        return int(time.strftime("%H"))

    def getTimeStamp(self) -> int:
        """时间戳"""
        t = int(time.time() * 1000)
        return t

    def json_extractor(self, obj, expr):
        """
        jsonpath提取
        :param obj: json对象
        :param expr: 表达式
        :return:
        """
        return jsonpath.jsonpath(obj, expr)

    def operate_ini(self, section, key, value=None, types=1):
        """
        配置文件ini操作
        :param section: 区块名称
        :param key: 名字
        :param value: 值
        :param types: 1：获取 0:修改
        :return:
        """
        conf = configparser.ConfigParser()  # 类的实例化
        conf.read(config_ini_dir)
        if types == 1:
            return conf.get(section, key)
        elif types == 0:
            conf.set(section, key, value)
            conf.write(open(config_ini_dir, 'w', encoding='utf-8'))


    def erms_all_robots_online_info(self):
        """
        获取erms全部在线的机器人信息
        :return:
        """
        info = []
        for robot in self.re1(self.url['robots']).json()['result']['robotResources']:
            if robot['status'] == 'online':
                info.append(robot)
        self.info(f'当前在线的AMR：{info}')
        return info

    def erms_robot_id(self, number):
        """
        获取erms指定机器人的id
        number: 机器人号码
        :return:
        """
        for info in self.erms_all_robots_online_info():
            if info['number'] == number:
                self.info(f"erms对应的ip：{info['number']} {info['id']}")
                return info['id']

    def erms_robot_sn(self, number):
        """
        获取erms指定机器人的sn
        number: 机器人号码
        :return:
        """
        for info in self.erms_all_robots_online_info():
            if info['number'] == number:
                return info['sn']

    def erms_robot_ip(self, resourceId):
        """
        获取erms指定机器人的ip
        :param resourceId: erms机器人id
        :return:
        """
        for ips in self.re1(self.url['connections']).json()['result']['connections']:
            if ips['resourceId'] == resourceId:
                return ips['ip']

    def agent_robot_finish(self, robotcode):
        """
        提前到达
        :param robotcode: 机器人code
        :return:
        """

        self.info(f'当前在线的AMR{robotcode}')
        self.info('获取erms的机器人id')
        erms_robot_id = self.erms_robot_id(robotcode)

        self.info('获取erms的机器人ip')
        ips = self.erms_robot_ip(erms_robot_id)
        if ips is not None:
            self.info('提前到达')
            self.url['finish']['url'] = self.url['finish']['url'].replace('agent', ':'.join([ips,'7000']))
            self.re1(self.url['finish'])
        else:
            self.error(f'机器人{robotcode}：未在线')

    def mktimes(self, st):
        """
        日期时间转换时间戳
        :param st 日期时间
        :return:
        """
        dt = time.strptime(st, "%Y-%m-%d %H:%M:%S")
        t = time.mktime(dt)
        return t

if __name__ == '__main__':
    f = Base('mysql', '1', 'jd_api', 'sy_test')
    print(select_issou())
    f.vx_inform(select_issou())

# -*- coding: utf-8 -*- 
# @Time : 2022/5/5 17:07 
# @Author : Yu yang
# @File : jd.py

import datetime
import random
import time

import jsonpath
import requests
from base.base import Base


class Jd(Base):
    # 拣货点数量
    station_number = 0

    def receivePicking1(self, tag: int):
        """
        下单
        :param tag: 任务类型
        :return:
        """
        t = self.getTimeStamp()
        self.url['receivePicking']['json']['taskNo'] = t
        self.url['receivePicking']['json']['tagType'] = tag
        self.url['receivePicking']['json']['cutOffTime'] = t + (60000 * 10)
        staion = ['01-01', '07-01', '013-01', '02-01', '08-01', '014-01',
                  '03-01', '09-01', '015-01', '04-01', '010-01', '016-01',
                  '05-01', '011-01', '017-01', '06-01', '012-01', '018-01', ]
        data = []
        for i in range(1, 10):
            data.append(staion[random.randint(0, 17)])
        data = list(set(data))
        self.url['receivePicking']['json']['detailList'] = data

        receivePicking = self.re1(self.url['receivePicking'])
        self.info(f'下单结果：{receivePicking.json()}')
        return receivePicking

    def receivePicking(self, tag: int):
        """
        下单
        :param tag: 任务类型
        :return:
        """
        t = self.getTimeStamp()
        self.url['receivePicking']['json']['taskNo'] = t
        self.url['receivePicking']['json']['tagType'] = tag
        self.url['receivePicking']['json']['cutOffTime'] = t + (60000 * 10)
        receivePicking = self.re1(self.url['receivePicking'])
        self.info(f'下单结果：{receivePicking.json()}')

    def picking(self, sql: str):
        """
        拣货确认
        :param sql: 查询到达拣货点
        :return:
        """
        # picking_arrive = self.select('select t1.robot_code as robotCode,t2.internal_station_name as stationName '
        #                              'from t_robot_task t1,t_robot_task_detail t2 where t1.id=t2.task_id and '
        #                              't1.biz_type="PICK_LOCATION" and t1.`status`=200 and t2.`status`=100 and '
        #                              't2.arrival_time is not null', fetch=False)
        picking_arrive = self.select(sql, fetch=False)
        self.info(f'到达拣货点信息：{picking_arrive}')
        if len(picking_arrive) >= 1:
            for info in picking_arrive:
                time.sleep(2)
                self.url['pickStationFinish']['json']['robotCode'] = info[0]
                self.url['pickStationFinish']['json']['stationName'] = info[1]
                pickStationFinish = self.re1(self.url['pickStationFinish'])
                self.info(f'拣货结果：{pickStationFinish.json()}')
        # 查询机器人上次拣货完成时间或者投线完成且非充电中
        # 查询当前机器人任务是否拣选中，查看与接单时间间隔

        # 查询是否拣选完成，拣选完成时间与当前时间间隔

    def unload(self, sql: str):
        """
        到达卸货点
        :param sql: 查询到达卸货点
        :return:
        """
        unload_arrive = self.select(sql, fetch=False)

        if len(unload_arrive) >= 1:
            self.info(f'到达卸货点信息：{unload_arrive}')
            for amrid in unload_arrive:
                self.url['freedAMR']['json']['robotCode'] = amrid[0]
                freedAMR = self.re1(self.url['freedAMR'])
                self.info(f'卸货结果：{freedAMR.json()}')
                time.sleep(3)
                self.receivePicking1(1)
                # for i in range(10):
                #     time.sleep(6)
                #     # print(jsonpath.jsonpath(self.robot_start(amrid[0]), '$..name'))
                #     data = jsonpath.jsonpath(self.robot_start(amrid[0]), '$..name')
                #     if data:
                #         if data[0][0:2] == 'go':
                #             self.info('前往停车区')
                #             self.receivePicking(1)
                #             break
                #         if data[0][0:2] == 'go':
                #             self.info('前往充电区')
                #             self.receivePicking(1)
                #             break

    def robot_start(self, resourceId: str):
        """
        查询指定机器人状态
        :param resourceId: 机器人编号获取创建机器人生成的随机数
        :return:
        """
        # resourceId 随机生成.映射robot
        robot = {"018": "81b5a771-e7af-4eff-b2d7-0124cd820e23"}
        self.url['jobs']['url'] = str(self.url['jobs']['url']).replace(
            'resourceId=81b5a771-e7af-4eff-b2d7-0124cd820e23', f'resourceId={robot[resourceId]}')
        re = self.re1(self.url['jobs'])
        return re.json()

    def count_task(self):
        """统计任务数量"""
        t = int(time.mktime(datetime.date.today().timetuple()) * 1000)
        self.url['page']['json']['lastFinishTime'][0] = t - 21600000
        self.url['page']['json']['lastFinishTime'][1] = t + 64800000
        self.url['page']['json']['lastFinishTimeBegin'] = t - 21600000
        self.url['page']['json']['lastFinishTimeEnd'] = t + 64800000
        re = self.re1(self.url['page']).json()['result']['totalCount']
        return re

    def count_2_task(self):
        t = int(time.mktime(datetime.date.today().timetuple()) * 1000)
        token = jsonpath.jsonpath(self.re1(self.url['login']).json(), '$..token')
        self.url['page1']['json']['createStartTime'] = t - 21600000
        self.url['page1']['json']['createEndTime'] = t + 64800000
        self.url['page1']['headers']['token'] = token[0]

        re = self.re1(self.url['page1']).json()['result']['totalCount']
        return re

    def unload_amr(self):
        """1.0
        通过机器人目标点及机器人状态判断是否到达
        到达拣货点：拣货
        到达停车区：下单
        """

        url = 'http://192.168.98.198:8070/robotManager/getRobotList'
        headers = {"Content-Type": "application/json"}
        json = {"timeout": 3000, "pageNumber": 1, "pageSize": 100, "robotCode": "", "mapName": ""}
        re = requests.post(url, headers=headers, json=json).json()
        # 遍历机器人的状态
        for amr_start in re['result']['items']:

            # AMR在线且到达状态
            if amr_start['baseStatus'] == '到达' and amr_start['startWork'] == True:
                # 判断到达目标点为卸货点****
                if amr_start['currentTargetName'][0:3] == '卸货点':
                    self.url['freedAMR']['json']['robotCode'] = amr_start['robotCode']
                    freedAMR = self.re1(self.url['freedAMR'])
                    self.info(f'卸货结果：{freedAMR.json()}')
            # AMR在线且目标点为停车区且空闲
            if amr_start['baseStatus'] == '空闲' and amr_start['currentTargetName'][0:3] == '停车区' and amr_start[
                'startWork'] == True:
                time.sleep(3)
                self.info('到达停车区')
                self.station_number += len(jsonpath.jsonpath(self.receivePicking1(1).json(), '$..pickStationNo'))

    def get_robot_id(self) -> dict:
        """
        返回字典类型的机器人编号和对应的机器人id
        :return:
        """
        re = self.re1(self.url['robots'])
        return dict(
            zip(
                jsonpath.jsonpath(re.json()['result']['robotResources'], '$..number'),
                jsonpath.jsonpath(re.json(), '$..id')
            )
        )


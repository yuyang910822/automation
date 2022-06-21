# -*- coding: utf-8 -*- 
# @Time : 2022/5/5 17:07 
# @Author : Yu yang
# @File : jd.py
import sys

from common.runemail import runEmail_text

from base.basePackage import Base

import datetime
import random
import sys
import time

import jsonpath
import requests


class Jd(Base):
    # 拣货点数量

    def receivePicking1(self, tag: int):
        """
        下单
        :param tag: 任务类型
        :return:
        """
        # 生成随机储位任务
        staion = ['01-01', '02-01', '04-01', '05-01', '07-01',
                  '08-01']
        data = ['08-01']
        for i in range(1, 10):
            data.append(staion[random.randint(0, 5)])
        data = list(set(data))

        t = self.getTimeStamp()
        self.url['receivePicking']['json']['taskNo'] = t
        self.url['receivePicking']['json']['tagType'] = tag
        self.url['receivePicking']['json']['cutOffTime'] = t + (60000 * 10)
        self.url['receivePicking']['json']['detailList'] = data
        self.re1(self.url['receivePicking'])

    def receivePicking(self, tag: int):
        """
        下单
        :param tag: 任务类型
        :return:
        """
        # 生成随机储位任务

        data = ['P01-01', 'P02-01', 'P03-01']
        t = self.getTimeStamp()
        self.url['receivePicking']['json']['taskNo'] = t
        self.url['receivePicking']['json']['tagType'] = tag
        self.url['receivePicking']['json']['cutOffTime'] = t + (60000 * 10)
        self.url['receivePicking']['json']['detailList'] = data
        self.re1(self.url['receivePicking'])

    def picking(self, sql: str, tag=1):
        """
        拣货确认且最后一个拣货点拣货完成下单
        :param sql: 查询到达拣货点
        :param tag: 下单类型
        :return:
        """
        picking_arrive = self.select(sql, fetch=False)
        if len(picking_arrive) >= 1:
            self.info(f'到达拣货点信息：{picking_arrive}')
            for info in picking_arrive:
                self.url['pickStationFinish']['json']['taskList'].clear()
                time.sleep(2)
                self.url['pickStationFinish']['json']['robotCode'] = info[0]
                self.url['pickStationFinish']['json']['stationName'] = info[1]
                result = self.re1(self.url['pickStationFinish'])
                # 兼容多任务版本确认拣货需要传递taskList
                self.debug(result.json()['status']['statusCode'])
                self.debug(type(result.json()['status']['statusCode']))
                if result.json()['status']['statusCode'] != 0:
                    self.warning('当前任务为多任务，入参加入taskNo')
                    self.url['pickStationFinish']['json']['taskList'][0]['taskNo'] = \
                        jsonpath.jsonpath(self.select_task_status(info[0]), "$..originWaveNo")[0]
                    self.re1(self.url['pickStationFinish'])
                #     self.warning('当前任务为多任务，入参加入taskNo')
                #     picking_id = self.select(f"select id,origin_wave_no from t_picking where parent_task_no = (select "
                #                              f"origin_wave_no from t_picking where `status` =200 and robot_code={info[0]})",
                #                              fetch=False)
                #     self.debug(f'当前机器人：{info[0]}对应的pickingid：{picking_id}')
                #     for id in picking_id:
                #         stationname = str(self.select(f'SELECT t_picking_detail.station_name from t_picking_detail '
                #                                       f'where picking_id ={id[0]}', fetch=False))
                #         if info[1] in stationname:
                #             self.url['pickStationFinish']['json']['taskList'].append(
                #                 {"taskNo": id[1], "passagewayTaskNo": "P1647342851-巷道拣货点0",
                #                  "pickingFlag": "0"})
                #     self.re1(self.url['pickStationFinish'])
                if info[1] == '08-01':
                    self.receivePicking1(tag)
                # if info[1] == 'P03-01':
                #     self.receivePicking(tag)
                #     self.receivePicking(tag)
                #     self.receivePicking(tag)
                #     self.receivePicking(tag)

    def picking1(self, sql: str, tag=1):
        """
        拣货确认且最后一个拣货点拣货完成下单
        :param sql: 查询到达拣货点
        :param tag: 下单类型
        :return:
        """
        picking_arrive = self.select(sql, fetch=False)
        if len(picking_arrive) >= 1:
            self.info(f'到达拣货点信息：{picking_arrive}')
            for info in picking_arrive:
                self.url['pickStationFinish']['json']['taskList'].clear()
                time.sleep(2)
                self.url['pickStationFinish']['json']['robotCode'] = info[0]
                self.url['pickStationFinish']['json']['stationName'] = info[1]
                picking_id = self.select(f"select id,origin_wave_no from t_picking where parent_task_no = (select "
                                             f"origin_wave_no from t_picking where `status` =200 and robot_code={info[0]})",
                                             fetch=False)
                self.debug(f'当前机器人：{info[0]}对应的pickingid：{picking_id}')
                for id in picking_id:
                    stationname = str(self.select(f'SELECT t_picking_detail.station_name from t_picking_detail '
                                                      f'where picking_id ={id[0]}', fetch=False))
                    if info[1] in stationname:
                        self.url['pickStationFinish']['json']['taskList'].append(
                                {"taskNo": id[1], "passagewayTaskNo": "P1647342851-巷道拣货点0",
                                 "pickingFlag": "0"})
                self.re1(self.url['pickStationFinish'])
                if info[1] == 'P03-01':
                    self.receivePicking(tag)
                    self.receivePicking(tag)
                    self.receivePicking(tag)
                    self.receivePicking(tag)

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
                time.sleep(2)
                self.url['freedAMR']['json']['robotCode'] = amrid[0]
                self.re1(self.url['freedAMR'])
                # self.receivePicking1(1)

    def robot_start(self, resourceId: str):
        """
        查询指定机器人状态
        :param resourceId: 机器人编号获取创建机器人生成的随机数
        :return:
        """
        # resourceId 随机生成.映射robot
        # robot = {"018": "81b5a771-e7af-4eff-b2d7-0124cd820e23"}
        self.url['charging_jobs']['url'].split()
        self.url['charging_jobs']['url'] = str(self.url['jobs']['url']).replace(
            'resourceId=81b5a771-e7af-4eff-b2d7-0124cd820e23', f'resourceId={self.get_robot_id()[resourceId]}')
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

    def charging_count(self):
        """
        统计充电次数
        :return:
        """
        numeber = 0

        for i in self.re1(self.url['charging_jobs']).json()['result']['jobs']:
            print(i)
            st = ' '.join([i['readyTime'].split('+')[0].split('T')[0], i['readyTime'].split('+')[0].split('T')[1]])
            timestamps = self.mktimes(st)
            start_timestamps = self.mktimes(self.startTime)
            end_timestamps = self.mktimes(self.endTime)
            if start_timestamps < timestamps < end_timestamps:
                numeber += 1
        return numeber

    def count_2_task(self):
        """
        1.0统计任务
        :return:
        """
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
                self.receivePicking1(1)

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

    def exceptionHandle(self):
        """
        异常监控
        :return:
        """

        handle = self.select('select * from t_exception_handle where `status` =0', fetch=False)
        if handle is not None:
            for handle_id in handle:
                time.sleep(5)
                # 拼接获取异常处理入参
                self.url['get']['url'] = 'get/'.join([self.url['get']['url'].split('get')[0], str(handle_id[0])])
                # 通过异常类型关联异常处理方法
                handle_info = self.re1(self.url['get']).json()['result']
                if handle_info['exceptionTypeDesc'] == "docking失败，并且无法识别容器编号":
                    self.url['handle']['json'] = handle_info
                    self.url['handle']['json']['containerCode'] = "111"
                    self.re1(self.url['handle'])
                elif handle_info['exceptionTypeDesc'] == '未知异常':
                    self.url['handle']['json'] = handle_info
                    self.re1(self.url['handle'])

            # elif exception['exceptionTypeDesc'] == '未知异常':
            #     pass
            # elif exception['exceptionTypeDesc'] == '未知异常':
            #     pass
            # elif exception['exceptionTypeDesc'] == '未知异常':
            #     pass
            # elif exception['exceptionTypeDesc'] == '未知异常':
            #     pass
            # elif exception['exceptionTypeDesc'] == '未知异常':
            #     pass
            # elif exception['exceptionTypeDesc'] == '未知异常':
            #     pass
            # elif exception['exceptionTypeDesc'] == '未知异常':
            #     pass

    def get_amr_tag(self, tags):
        """
        获取配置指定AMR的tag
        :param tags 对应模式的tag
        :return:
        """
        # 空闲在线AMR id
        data = self.re1(self.url['robots']).json()
        for amrid in data['result']['robotResources']:
            # 获取tag
            self.url['robots_tag']['url'] = 'robots/'.join(
                [self.url['robots_tag']['url'].split('robts')[0], amrid['id']])
            # 一台AMR配置多个tag 满足一个就下单并终止
            for tag in tags:
                if tag in self.re1(self.url['robots_tag']).json()['result']['robotResource']['tags']:
                    # 满足则下单
                    self.receivePicking1(random.randint(2, 3))
                    break

    def run(self, run_time=18):
        """发送邮件"""
        if self.getTime() == run_time and self.operate_ini('status', 'email_status') == 'False':
            t = time.mktime(datetime.date.today().timetuple())
            startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t - 21600))
            endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t + 64800))
            number = self.select(
                f'SELECT * FROM t_picking WHERE `status` = 500 and create_time>"{startTime}" and  create_time<"{endTime}";',
                fetch=False)
            print(
                f'SELECT * FROM t_picking WHERE `status` = 500 and create_time>"{startTime}" and  create_time<"{endTime}";')
            print('测试报告已发出，更新状态')
            info = f'Hi all:\n' \
                   f'\n' \
                   f'\t今日京东水饮流程稳定性测试完成：\n' \
                   f'\t     开始时间（{(datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")}|18:00' \
                   f':00）\n' \
                   f'\t     结束时间（{self.getDateTime()}）\n' \
                   f'\t     共执行任务数量：{len(number)}单\n' \
                   f'\t     共完成充电任务：{self.charging_count}'
            runEmail(info, ''.join(['【京东2.0水饮仓】--', '稳定性测试' + str(time.strftime("%Y-%m-%d"))]))
            print('测试报告已发出，更新状态')
            self.operate_ini('status', 'email_status', 'True', types=0)
        elif self.operate_ini('status', 'email_status') == 'True' and self.getTime() != run_time:
            print('重新开始，初始化状态')
            self.operate_ini('status', 'email_status', 'False', types=0)

    def select_task_status(self, robotcode=None, status=None, pageSize=10):
        """
        查询指定AMR状态的任务信息
        :param pageSize: 条数
        :param robotcode: 机器人id
        :param status: 状态
        :return: 指定amr编号任务信息json
        """
        self.url['page']['json'] = {"robotCode": robotcode, "status": status, "pageNumber": 1, "pageSize": pageSize}
        return self.re1(self.url['page']).json()

    def conut_run_task_time(self):
        """统计运行时间"""
        count_time = {}
        strs = ''
        t = time.mktime(datetime.date.today().timetuple())
        startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t - 21600))
        endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t + 64800))
        for i in self.select(
                "SELECT robot_code,picking_start_time,finish_time FROM t_picking "
                f"where create_time> '{startTime}' and create_time<'{endTime}' and `status`=500 ;"
                , fetch=False):

            if i[0] in count_time:
                count_time[i[0]][0] = count_time[i[0]][0] + int(i[2].timestamp()) - int(i[1].timestamp())
                count_time[i[0]][1] += 1
            else:
                count_time[i[0]] = [int(i[2].timestamp()) - int(i[1].timestamp())]
                count_time[i[0]].append(1)

        for j in count_time:
            seconds = count_time[j][0] % (24 * 3600)
            hour = count_time[j][0] // 3600
            count_time[j][0] %= 3600
            minutes = count_time[j][0] // 60
            seconds %= 60
            count_time[j][0] = "%02d:%02d:%02d" % (hour, minutes, seconds)

        for k in count_time:
            strs += f'\t     AMR:{k} | 共执行{count_time[k][0]} | 任务数量：{count_time[k][1]}单\n'

        return strs


if __name__ == '__main__':
    auto = Jd('sy_mysql_prod', 'test_水印', 'jd_multitask_api', 'sy_prod')
    print(auto.charging_count)

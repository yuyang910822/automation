# -*- coding: utf-8 -*- 
# @Time : 2022/6/17 9:39 
# @Author : Yu yang
# @File : jd_multitask_one.py

import random
import time, datetime

import requests

from base.jd import Jd
from common.runemail import runEmail_text


class Jd_multitask(Jd):
    # 未发出报告
    start = 0

    def jd_multitask(self):
        """
        京东多任务：合流&非合流
        :return:
        """

        while True:
            time.sleep(5)

            # 提前到达
            # for info in self.select_task_status(status=200)['result']['items']:
            #     self.info(f'拣货中机器人{info["robotCode"]}任务号：{info["id"]}')
            #     self.url['pickingLog']['json']['pickingId'] = info['id']
            #     data = self.re1(self.url['pickingLog']).json()['result']['details'][-1]
            #     self.info(f"上箱：{data['bizName']}----{data['content']}")
            #     if data['bizName'] == '上箱' and data['content'] == '任务begin,PICK_LOADING':
            #         time.sleep(5)
            #         self.agent_robot_finish(info['robotCode'])
            #     self.info(f"拣货：{data['bizName']}----{data['content']}")
            #     if data['bizName'] == '拣选' and data['content'] == '任务begin,PICK_LOCATION':
            #         time.sleep(5)
            #         self.agent_robot_finish(info['robotCode'])
            # for info in self.select_task_status(status=300)['result']['items']:
            #     self.info(f'拣选完成机器人{info["robotCode"]}任务号：{info["id"]}')
            #     self.url['pickingLog']['json']['pickingId'] = info['id']
            #     data = self.re1(self.url['pickingLog']).json()['result']['details'][-1]
            #     self.info(f"卸货：{data['bizName']}----{data['content']}")
            #     if data['bizName'] == '卸货' and data['content'] == '任务begin,PICK_UNLOADING':
            #         time.sleep(5)
            #         self.agent_robot_finish(info['robotCode'])

            # 异常处理
            # 处理异常
            self.exceptionHandle()

            # 拣货点确认
            self.picking('select t1.robot_code as robotCode,t2.internal_station_name as stationName from t_robot_task '
                         't1,t_robot_task_detail t2 where t1.id=t2.task_id and t1.biz_type="PICK_LOCATION" and '
                         't1.`status`=200 and t2.`status`=100 and t2.arrival_time is not null', tag=2)

            # 邮件发送
            if self.getTime() == 18 and self.operate_ini('status', 'multitask_email_status1') == 'False':
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
                       f'\t今日京东非合流稳定性测试完成：\n' \
                       f'\t     开始时间（{(datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")}|18:00' \
                       f':00）\n' \
                       f'\t     结束时间（{self.getDateTime()}）\n' \
                       f'\t     共执行任务数量：{len(number)}单\n' \
                       f'\t     共完成充电任务：{self.charging_count}'
                runEmail_text(info, ''.join(['【京东2.0非合流】--', '稳定性测试' + str(time.strftime("%Y-%m-%d"))]))
                print('测试报告已发出，更新状态')
                self.operate_ini('status', 'multitask_email_status1', 'True', types=0)
            elif self.operate_ini('status', 'multitask_email_status1') == 'True' and self.getTime() != 18:
                print('重新开始，初始化状态')
                self.operate_ini('status', 'multitask_email_status1', 'False', types=0)


if __name__ == '__main__':
    auto = Jd_multitask('sy_mysql_prod', 'multitask', 'jd_multitask_api', 'sy_prod')
    auto.jd_multitask()

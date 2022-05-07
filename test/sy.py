# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/7/6 15:39
  @Auth : 于洋
  @File : core_competence.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""

import jsonpath as jsonpath
import time
import time,datetime
from base.base import Base
from base.jd import Jd
from common.vx import vx_inform


class Sy(Jd):

    # 未发出报告
    start = 0

    def sy_atutomationa(self):
        """
        水印仓流程测试
        :return:
        """

        while True:
            time.sleep(5)
            self.picking('select t1.robot_code as robotCode,t2.internal_station_name as stationName from t_robot_task '
                         't1,t_robot_task_detail t2 where t1.id=t2.task_id and t1.biz_type="PICK_LOCATION" and '
                         't1.`status`=200 and t2.`status`=100 and t2.arrival_time is not null')

            self.unload("select t1.robot_code as robotCode from t_robot_task t1,t_robot_task_detail t2 where "
                        "t1.id=t2.task_id and t1.biz_type='PICK_UNLOADING' and t1.`status`=200 and t2.`status`=100 "
                        "and t2.arrival_time is not null;")

            if self.getTime() == 19 and self.start == 0:
                task_quantity = self.count_task()
                vx_inform(f'今日京东水印流程稳定性测试完成：\n'
                          f'开始时间（{(datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")}|18:00'
                          f':00）\n结束时间（{self.getDateTime()}）\n'
                          f'共执行任务数量：{task_quantity}单\n'
                          f'平均耗时：{int(1440 / task_quantity)}分')
                print('测试报告已发出，更新状态')
                self.start = 1
            elif self.getTime() == 0 and self.start == 1:
                print('重新开始，初始化状态')
                self.start = 0



if __name__ == '__main__':
    auto = Sy('mysql', 'test_水印', 'jd_api', 'sy_test')
    auto.sy_atutomationa()

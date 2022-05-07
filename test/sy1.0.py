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
            # 查询待拣货AMR
            self.picking("select t1.robot_code as robotCode,t2.internal_station_name as stationName,(select "
                         "t_wave.original_wave_no from t_wave where t_wave.id=t1.wave_id) taskNo from "
                         "t_robot_task t1,t_robot_task_detail t2 where t1.id=t2.task_id and t1.`status`=200 "
                         "and t2.`status`=100 and t2.arrival_time >0")
            # 查询到达拣货点或停车区的AMR触发对应动作
            self.unload_amr()

            # 企业微信输出测试结果
            if self.getTime() == 18 and self.start == 0:
                vx_inform(f'今日京东水印流程自动化测试完成：\n'
                          f'开始时间--结束时间\n'
                          f'   0       24  \n'
                          f'共执行任务数量：{self.count_task()}')
                print('测试报告已发出，更新状态')
                self.start = 1
            elif self.getTime() == 0 and self.start == 1:
                print('重新开始，初始化状态')
                self.start = 0


if __name__ == '__main__':
    auto = Sy('sy_mysql_prod', 'cnagku_sy', 'jd_api', 'sy_prod')
    auto.sy_atutomationa()

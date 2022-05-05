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


def sy_atutomationa(self):
    """
            到达点位
            :return:
            """
    while True:
        time.sleep(5)
        # 待卸货AMR
        amr_info = []
        picking_arrive = self.select('select t1.robot_code as robotCode,t2.internal_station_name as stationName,'
                                     '(select t_wave.original_wave_no from t_wave where t_wave.id=t1.wave_id) '
                                     'taskNo,t2.arrival_time from t_robot_task t1,t_robot_task_detail t2 where '
                                     't1.id=t2.task_id and t1.`status`=200 and t2.`status`=100 and '
                                     't2.arrival_time is not null and t2.leave_time is null;', fetch=False)
        self.info(f'到达拣货点信息：{picking_arrive}')
        if picking_arrive is not None:
            for re in picking_arrive:
                # 添加到达拣货的AMR，用于拣货确认
                amr_info.append(re[0])
                self.url['pickStationFinish']['json']['robotCode'] = re[0]
                self.url['pickStationFinish']['json']['stationName'] = re[1]
                if self.re1(self.url['pickStationFinish']).json()['status']['statusCode'] != 0:
                    # 企业微信同步
                    pass
                    return

        if len(amr_info) > 0:
            for amr in amr_info:
                # 提前到达
                time.sleep(2)
                self.url['operateRobot_10']['json']['robotCode'] = amr
                if self.re1(self.url['operateRobot_10']).json()['status']['statusCode'] != 0:
                    # 企业微信同步
                    pass
                    return
                time.sleep(2)
                self.url['freedAMR']['json']['robotCode'] = amr
                if self.re1(self.url['freedAMR']).json()['status']['statusCode'] != 0:
                    # 企业微信同步
                    pass
                    return
                self.receivePicking(1)
        amr_info.clear()

        if self.getTime() >= '180000':
            # 提取今天任务数量 车号
            date = self.getDate()


if __name__ == '__main__':
    pass

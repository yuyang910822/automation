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
from datetime import datetime
import datetime
import time
from base.jd import Jd
from common.linux_operate import Linux
from common.runemail import runEmail
from common.vx import vx_inform


class Sy(Jd):
    """仓库--水印仓1.0"""

    # 标记是否发送邮件，0：fales 1：True
    start = 0

    def sy_atutomationa(self):
        """
        水印仓流程测试
        拣货--卸货--停车--下单
        :return:
        """

        while True:
            time.sleep(5)
            # 查询待拣货AMR信息进行遍历
            self.picking("select t1.robot_code as robotCode,t2.internal_station_name as stationName,(select "
                         "t_wave.original_wave_no from t_wave where t_wave.id=t1.wave_id) taskNo from "
                         "t_robot_task t1,t_robot_task_detail t2 where t1.id=t2.task_id and t1.`status`=200 "
                         "and t2.`status`=100 and t2.arrival_time >0")
            # 查询到达拣货点或停车区的AMR触发对应动作
            self.unload_amr()

            # 通过时间进行email发送，并修改标记状态
            if self.getTime() == 16 and self.start == 0:
                task_quantity = self.count_2_task()
                if task_quantity != 0:
                    info = f'Hi all:\n' \
                           f'\n' \
                           f'   今日京东水饮流程稳定性测试完成：\n' \
                           f'       开始时间（{(datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")}|18:00' \
                           f':00）' \
                           f'       结束时间（{self.getDateTime()}）\n' \
                           f'       共执行任务数量：{task_quantity}单\n' \
                           f'       拣货点：{self.station_number}个\n' \
                           f'       平均耗时：{int(1440 / task_quantity)}分\n'

                    runEmail(info, ''.join(['【京东1.0水饮仓】--', '稳定性测试' + str(time.strftime("%Y-%m-%d"))]))
                    print('测试报告已发出，更新状态')
                    # 任务状态
                    self.start = 1
                elif task_quantity == 0:
                    info = f'Hi all:\n' \
                           f'\n' \
                           f'   今日京东水饮流程稳定性测试完成：\n' \
                           f'       开始时间（{(datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")}|18:00' \
                           f':00）\n' \
                           f'       结束时间（{self.getDateTime()}）\n' \
                           f'       共执行任务数量：{task_quantity}单\n' \
                           f'       拣货点：{self.station_number}个\n'

                    runEmail(info, ''.join(['【京东1.0水印仓】--', '稳定性测试' + str(time.strftime("%Y-%m-%d"))]))
                    print('测试报告已发出，更新状态，任务数量：{}'.format(task_quantity))
                    self.start = 1

            elif self.getTime() == 0 and self.start == 1:
                print('初始化，初始化标记状态')
                self.start = 0

            Linux.linux_order(login=[['192.168.98.202', 'ld', 'ld', '002'],
                                     ], order='grep "收到到达目的地信息SessionID"  -A 1 '
                                              '/opt/raccoon/cluster/fta_server/logs/info/log-info.log |tail -n 2')

            #


if __name__ == '__main__':
    auto = Sy('sy_mysql_prod', 'cnagku_sy', 'jd_api', 'sy_prod')
    auto.sy_atutomationa()

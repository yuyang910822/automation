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


import time, datetime

from base.jd import Jd
from common.runemail import runEmail


class Jd_singletask(Jd):
    """
    京东单任务
    """
    # 未发出报告
    start = 0

    def sy_atutomationa(self):
        """
        水印仓流程测试
        :return:
        """

        while True:
            time.sleep(5)
            # 上箱点异常AMR

            # 到达拣货点AMR
            self.picking('select t1.robot_code as robotCode,t2.internal_station_name as stationName from t_robot_task '
                         't1,t_robot_task_detail t2 where t1.id=t2.task_id and t1.biz_type="PICK_LOCATION" and '
                         't1.`status`=200 and t2.`status`=100 and t2.arrival_time is not null', tag=1)

            # 到达投线点AMR
            self.unload("select t1.robot_code as robotCode from t_robot_task t1,t_robot_task_detail t2 where "
                        "t1.id=t2.task_id and t1.biz_type='PICK_UNLOADING' and t1.`status`=200 and t2.`status`=100 "
                        "and t2.arrival_time is not null;")

            # 投线点异常AMR

            # 空闲AMR下单

            if self.getTime() == 18 and self.operate_ini('status', 'singletask_email_status') == 'False':
                t = time.mktime(datetime.date.today().timetuple())
                startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t - 21600))
                endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t + 64800))
                number = self.select(
                    f'SELECT * FROM t_picking WHERE `status` = 500 and create_time>"{startTime}" and  create_time<"{endTime}";',fetch=False)
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
                       f'\t     共完成充电任务：{self.charging_count}\n' \
                       f'\n' \
                       f'AMR执行详细信息如下：\n' \
                       f'{self.conut_run_task_time()}'
                runEmail(info, ''.join(['【京东2.0标签拣选】--', '稳定性测试' + str(time.strftime("%Y-%m-%d"))]))
                print('测试报告已发出，更新状态')
                self.operate_ini('status', 'singletask_email_status', 'True', types=0)
            elif self.operate_ini('status', 'singletask_email_status') == 'True' and self.getTime() != 18:
                print('重新开始，初始化状态')
                self.operate_ini('status', 'singletask_email_status', 'False', types=0)


if __name__ == '__main__':
    auto = Jd_singletask('sy_mysql_prod', 'test_水印', 'jd_singletask_api', 'sy_prod')
    auto.sy_atutomationa()


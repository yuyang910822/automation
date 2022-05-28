# -*- coding: utf-8 -*- 
# @Time : 2022/5/26 23:57 
# @Author : Yu yang
# @File : jd_multitask.py
import random
import time, datetime

from base.jd import Jd
from common.runemail import runEmail


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
            # 处理异常
            self.exceptionHandle()

            # 到达拣货点AMR
            self.picking('select t1.robot_code as robotCode,t2.internal_station_name as stationName from t_robot_task '
                         't1,t_robot_task_detail t2 where t1.id=t2.task_id and t1.biz_type="PICK_LOCATION" and '
                         't1.`status`=200 and t2.`status`=100 and t2.arrival_time is not null')
            # 到达投线点AMR
            self.unload("select t1.robot_code as robotCode from t_robot_task t1,t_robot_task_detail t2 where "
                        "t1.id=t2.task_id and t1.biz_type='PICK_UNLOADING' and t1.`status`=200 and t2.`status`=100 "
                        "and t2.arrival_time is not null;")

            # 符合tag的空闲amr则下单
            self.get_amr_tag('COv0vWD6')

            # 发送邮件
            self.run()


if __name__ == '__main__':
    auto = Jd_multitask('sy_mysql_prod', 'test_水印', 'jd_api', 'sy_prod')
    auto.jd_multitask()


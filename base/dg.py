# -*- coding: utf-8 -*- 
# @Time : 2022/7/4 11:27 
# @Author : Yu yang
# @File : dg.py
import random
import time

from base.basePackage import Base


class Dg(Base):

    def receive(self, tag_type):
        """
        下单
        :return:
        """
        self.url['receive']['json'][0]['originNo'] = self.getTimeStamp()
        self.url['receive']['json'][0]['originType'] = int(tag_type)

        self.re1(self.url['receive'])

    def wave_unlock(self):
        """
        解锁波次
        :return:
        """
        # 未解锁波次
        for info in self.re1(self.url['wave_page']).json()['result']['items']:
            # 依次解锁
            self.url['updateLockStatus']['json']['idList'][0] = info['id']
            self.re1(self.url['updateLockStatus'])

    def picking(self, tag_type):
        """
        确认拣货
        :return:
        """

        picking_info = self.select("SELECT (tpd.picking_qty-tpd.picked_qty-tpd.lack_qty),tpd.id,t.id,t.business_id,"
                                   "tp.station_name,tp.internal_station_name,t.robot_code from t_robot_task "
                                   "t join t_robot_task_detail tp on t.id =tp.task_id join t_picking_detail tpd on "
                                   "tp.business_detail_id=tpd.id where t.`status`=200 and tp.arrival_time is not null "
                                   "and leave_time is NULL;",
                                   fetch=False)

        if len(picking_info) >= 1:
            for info in picking_info:
                if info[6] == 'MAX-001':
                    self.info(f'当前待拣选AMT信息：{info}')
                    time.sleep(2)
                    self.url['confirm']['json']['pickedQty'] = info[0]
                    self.url['confirm']['json']['pickingDetailId'] = info[1]
                    self.url['confirm']['json']['robotTaskId'] = info[2]
                    self.url['confirm']['json']['pickingId'] = info[3]
                    # 确认拣货
                    self.re1(self.url['confirm'])

                    # 二次确认
                    self.url['after_confirm']['json']['robotTaskId'] = info[2]
                    self.url['after_confirm']['json']['pickingId'] = info[3]
                    self.url['after_confirm']['json']['internalStationName'] = info[5]
                    self.re1(self.url['after_confirm'])

                    if info[4] == 'P55-01-1-1':
                    # 1: 总拣上箱 2：总拣不上箱
                    # # 单车随机切换
                    # tag_info = {1: [12,'总拣自动顶升',10], 2: [12,'总拣不上箱',1]}
                    # tag_info_number = random.randint(1, 2)
                    # tag = self.picking(tag_info[tag_info_number][0])
                    #
                    # if tag == 1:
                    #     # 目标流程启用
                    #     self.url['list']['json']['name'] = tag_info[1][1]
                    #     if self.re1(self.url['list']).json()['result'][0]['status'] != 200:
                    #         self.url['change']['url'] = self.url['change']['url'] + f'/{tag_info[1][-1]}/{200}'
                    #     # 冲突流程停用
                    #     self.url['list']['json']['name'] = tag_info[2][1]
                    #     if self.re1(self.url['list']).json()['result'][0]['status'] != 300:
                    #         self.url['change']['url'] = self.url['change']['url'] + f'/{tag_info[2][-1]}/{300}'

                    # 多车指定流程
                        self.receive(tag_type)
                        self.wave_unlock()
        return tag_type

    def operate(self):
        """
        系统操作处理：提前到达，异常处理
        :return:
        """

        for info in self.re1(self.url['robit_list']).json()['result']:
            time.sleep(2)
            self.info(f'系统待操作AMR：{info}')
            # 提前到达
            if info['arrivedStatus'] == 2 and info['robotNo']== 'MAX-001':
                time.sleep(2)
                self.info(f'导航中，准备提前到达：{info["robotNo"]}')
                self.url['operate']['json']['robotCode'] = info['robotNo']
                self.url['operate']['json']['command'] = "finish"
                self.re1(self.url['operate'])
            # 异常处理
            if '异常' in str(info) and info['robotNo'] == 'MAX-001':
                time.sleep(2)
                self.info(f'AMR异常，准备处理异常：{info["robotNo"]}')
                self.url['operate']['json']['robotCode'] = info['robotNo']
                self.url['operate']['json']['command'] = "resume_sub_task"
                self.re1(self.url['operate'])




    def update_process(self):
        tag_info = {1: 12, 2: 12}
        # 拣货点确认
        # 1: 总拣上箱 2：总拣不上箱
        tag_info_new = random.randint(1, 2)
        self.picking(tag_info[tag_info_new])





if __name__ == '__main__':
    f = Dg('dg_mysql_test','dg_picking','dg_api','dg_test')
    f.receive(12)

# -*- coding: utf-8 -*- 
# @Time : 2022/7/4 11:25 
# @Author : Yu yang
# @File : dg_picking.py
import random

from base.dg import Dg


class Dg_picking(Dg):
    """
    灯光拣选流程:
        总拣上箱： 自动上箱--拣货--自动卸货
        总拣不上箱：         拣货--手动卸货

    """

    def auto_test(self):
        """
        自动测试_灯光
        :return:
        """
        while True:
            # 系统操作
            self.operate()

            # 拣货点确认
            self.picking(12)


if __name__ == '__main__':
    f = Dg_picking('dg_mysql_test', 'dg_picking', 'dg_api', 'dg_test')
    f.auto_test()

# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/7/6 16:05 
  @Auth : 于洋
  @File : mysql.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
-------------------------------------------------
"""

import pymysql

from common.log import Log


class Mysql(Log):
    """数据库"""

    def __init__(self, mysql_data, name='日志', level='DEBUG', file=None):
        """
        初始化数据库
        """
        self.db = pymysql.connect(host=mysql_data['host'], user=mysql_data['user'],
                                  password=mysql_data['password'], port=mysql_data['port'],
                                  charset=mysql_data['charset'],database=mysql_data['database'])
        super(Mysql, self).__init__(name, level, file)
        # 创建游标
        self.c = self.db.cursor()

    def closes(self):
        """关闭游标"""
        self.db.close()
        self.c.close()

    def select(self, sql: str, fetch: bool=True):
        """
        执行sql
        :param sql: sql命令
        :param fetch: True:查询第一行 False：查询全部
        :return: 
        """""
        try:
            self.c.execute(sql)

            self.db.commit()
        except BaseException as e:
            self.error(f'{e}')
            self.db.rollback()
        else:
            if fetch:
                return self.c.fetchone()
            else:
                return self.c.fetchall()


if __name__ == '__main__':
    a = Mysql()
    print(a.select('SELECT * from test_jd_rcs.internal_external_station_mapping'))

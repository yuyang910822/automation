# -*- coding: utf-8 -*- 
# @Time : 2022/4/29 21:34 
# @Author : Yu yang
# @File : issou.py

import jira
import jsonpath


def select_issou():
    """
    计算"报告人"为当前用户的具体项目的DI值
    :return:
    """
    data = []
    j = jira.JIRA(server="https://issue.forwardx.ai", basic_auth=('yuyang', 'Han123123!'))

    #
    for i in j.search_issues(
            f'reporter in (yuyang, yezhihua, wangrenjie, lichangxu, zhaojidong, gaoxiaohong) ORDER BY status DESC, '
            f'created DESC', maxResults=1000):
        print(i)
        issues = j.issue(i)
        # 获取对应问题单的状态
        if str(issues.fields.status) == '回归测试':
            # 获取对应状态的严重程度

            tiele = jsonpath.jsonpath(issues.raw, '$..summary')[0]
            data.append(issues.key + '' + tiele + '--' + str(issues.fields.assignee) + ' ')
    return str(data).strip('[').strip(']').replace(', ', '\n')


if __name__ == '__main__':
    print(select_issou())

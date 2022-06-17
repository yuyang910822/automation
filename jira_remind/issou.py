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

    stre = ''
    j = jira.JIRA(server="https://issue.forwardx.ai", basic_auth=('yuyang', 'Han123123!'))

    for i in j.search_issues('status = 回归测试 AND reporter in (membersOf(QT)) order by created DESC'):
        issues = j.issue(i)
        # 获取对应问题单的状态
        if str(issues.fields.status) == '回归测试':
            tiele = jsonpath.jsonpath(issues.raw, '$..summary')[0]
            # data.append(issues.key + '' + tiele + '----' + str(issues.fields.assignee) + ' ')
            data.append(str(issues.fields.assignee))
    # for i in j.search_issues('status in (确认中, 执行中) AND "经办人(测试人员)" in (yezhihua, zhaojidong, lichangxu, gaoxiaohong, '
    #                          'yuyang) order by created DESC'):
    #     issues = j.issue(i)
    #     print(issues,jsonpath.jsonpath(issues.raw, '$..summary')[0],issues.fields.status,issues.fields.assignee)
    #     # 获取对应问题单的状态
    #     if str(issues.fields.status) == '执行中' or str(issues.fields.status)=='确认中' :
    #         tiele = jsonpath.jsonpath(issues.raw, '$..summary')[0]
    #         # data.append(issues.key + '' + tiele + '----' + str(issues.fields.assignee) + ' ')
    #         data.append(str(issues.fields.assignee))
    # for i in set(data):
    #     print(i)
    #     stre += f'{i.split("(")[-1].split(")")[0]}:\n  待验证问题单数:{data.count(i)}单\n'
    for i in set(data):
        stre += f'{i.split("(")[-1].split(")")[0]}:\n  待验证问题单数:{data.count(i)}单\n'

    return stre


if __name__ == '__main__':
    print(select_issou())
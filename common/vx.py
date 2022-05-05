# -*- coding: utf-8 -*- 
# @Time : 2022/4/29 21:58 
# @Author : Yu yang
# @File : vx.py

from jira_remind.issou import *


def vx_inform(info):
    import json
    import requests

    corp_id = 'wwfe85fd2d948fbb07'
    corp_secret = '7Stqr1vMwg46EkeCngjgRgxUZWsh9kyTFrhYvkRDSOU'
    agent_id = '1000002'

    resp = requests.get(
        f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}')
    js = json.loads(resp.text)
    if js["errcode"] == 0:
        access_token = js["access_token"]
        expires_in = js["expires_in"]

        data = {
            "touser": "@all",
            "msgtype": 'text',
            "agentid": agent_id,
            "text": {
                "content": info
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}',
                             json=data)
        js = json.loads(resp.text)
        if js["errcode"] == 0:
            return js


if __name__ == '__main__':
    vx_inform(f'今日待回归问题如下，版本未转测等请忽略：\n{select_issou()}'.replace("'", ''))

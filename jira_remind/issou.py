import os
import sys
import time
from datetime import datetime

sys.path.append('/home/ld/.local/lib/python3.6/site-packages')
sys.path.append('/home/ld/PycharmProjects/automation')
import jira
import jsonpath

from base.basePackage import Base
from common.runemail import runEmail_text
from chinese_calendar import is_workday
from pyecharts.charts import Bar
from pyecharts import options as opts

class Jira(Base):

    def get_issour(self):
        """
        获取问题单
        :return:
        """
        j = jira.JIRA(server="https://issue.forwardx.ai", basic_auth=('yuyang', 'Han123123!'))

        jira_info = {"王仁杰": [], "于洋": [], "叶志华": [], "赵吉东": [], "李长旭": [], "高晓红": []}
        jira_info_count = {"王仁杰": [], "于洋": [], "叶志华": [], "赵吉东": [], "李长旭": [], "高晓红": []}
        for i in j.search_issues(
                'status in (修改实施, 修改审核, 回归测试) AND reporter in (lichangxu, wangrenjie, yuyang, yezhihua, '
                'zhaojidong, gaoxiaohong) order by created DESC', maxResults=10000):
            issues = j.issue(i)

            names = jsonpath.jsonpath(issues.raw, '$..reporter')[0]['displayName'].split('(')[-1].split(')')[0]

            if names in jira_info:
                jira_info[names].append(str(issues.fields.status))
            else:
                jira_info[names] = [str(issues.fields.status)]

        for j in jira_info:
            print(j)
            jira_info_count[j].append(jira_info[j].count('修改实施'))
            jira_info_count[j].append(jira_info[j].count('修改审核'))
            jira_info_count[j].append(jira_info[j].count('回归测试'))
        print(jira_info_count)
        return jira_info_count

    def generate_html(self, info):
        """
        生成HTML试图
        :param info:
        :return:
        """
        bar = Bar()

        # 用列表来保持
        bar.add_xaxis(["修改实施", "修改审核", "回归测试"])
        # 添加y轴数据
        bar.add_yaxis("王仁杰", [info['王仁杰'][0], info['王仁杰'][1], info['王仁杰'][2]])
        bar.add_yaxis("于洋", [info['于洋'][0], info['于洋'][1], info['于洋'][2]])
        bar.add_yaxis("叶志华", [info['叶志华'][0], info['叶志华'][1], info['叶志华'][2]])
        bar.add_yaxis("赵吉东", [info['赵吉东'][0], info['赵吉东'][1], info['赵吉东'][2]])
        bar.add_yaxis("李长旭", [info['李长旭'][0], info['李长旭'][1], info['李长旭'][2]])
        bar.add_yaxis("高晓红", [info['高晓红'][0], info['高晓红'][1], info['高晓红'][2]])

        # 设置标题
        bar.set_global_opts(title_opts=opts.TitleOpts(title="Jira问题单一览表"))

        bar.render(f"../jira_remind/html_info/jira{self.getDate()}.html")

    def send_jira(self):
        """
        发送
        :return:
        """

        while True:
            if is_workday(datetime.now().date()):
                if self.getTime() == 11 and self.operate_ini('status', 'jira_email_status') == 'False':
                    self.generate_html(self.get_issour())
                    path = os.path.join('../jira_remind/html_info', os.listdir('../jira_remind/html_info')[-1])
                    info = \
                        'Hi All:\n' \
                        '\t     待验证及需跟进推动问题，详见附件。'
                    runEmail_text(info,
                                  ''.join(['【系统集成测试】--', '待验证问题' + str(time.strftime("%Y-%m-%d"))]),
                                  'yuyang@forwardx.com',
                                  path)
                    self.info('更新状态：True')
                    self.operate_ini('status', 'jira_email_status', 'True', types=0)
                elif self.operate_ini('status', 'jira_email_status') == 'True' and self.getTime() != 14:
                    self.info('初始化状态：False')
                    self.operate_ini('status', 'jira_email_status', 'False', types=0)

if __name__ == '__main__':
    a = Jira('sy_mysql_prod', 'test_水印', 'jd_singletask_api', 'sy_prod')
    a.send_jira()
import os
import smtplib
import time
import unittest
from email import message
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from common.path import report_dir, test_dir


# def run_test():
    #     # 定义测试用例路径
    #
    #     # 存放报告的文件夹
    #     report_dir = '../report'
    #     discover = unittest.defaultTestLoader.discover(test_dir, pattern="test21.py", top_level_dir=None)
    #     # 报告命名时间格式化
    #     now = time.strftime("%Y-%m-%d %H~%M~%S")
    #     # 报告文件完整路径
    #     report_name = report_dir + '/' + now + 'result.html'
    #     with open(report_name, 'wb') as f:
    #         runner = HTMLTestRunner.HTMLTestRunner(stream=f, title=' 测试结果如下：', description='用例执行情况：')
    #         # 执行测试用例文件
    #         runner.run(discover)


def runEmail_text(info, title, email, accessory_path=None):
    """
    发送email文本
    :param info: 文本
    :param title: 标题
    :param email: 接收人
    :param accessory_path: 附件路径
    :return:
    """

    # file = open(file, 'rb')
    # file_data = str(file.read())
    # file.close()

    sender = 'yuyang@forwardx.com'

    mail = MIMEMultipart()
    mail['Subject'] = title
    mail['From'] = sender  # 发件人
    mail['To'] = email  # 收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工

    # 构造正文
    body = MIMEText(info, 'plain', 'utf8')

    # ③构造附件1
    if accessory_path:
        att1 = MIMEText(open(accessory_path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="jira.html"'
        mail.attach(att1)
    mail.attach(body)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect("smtp.exmail.qq.com", 25)  # 25 为 SMTP 端口号
        smtpObj.login(sender, 'AcgB5ZvhEsZNrYaf')
        smtpObj.sendmail(sender, email.split(','), mail.as_string())
        smtpObj.quit()
    except BaseException as e:
        print(e)
        print('fail')
    else:
        print('success')


def runEmail_html(file, title, email):
    """
    Email发送
    :return:
    """
    file = open(file, 'rb')
    file_data = file.read()
    file.close()
    body = MIMEText(file_data, 'html', 'utf8')

    # 构造邮件主体
    mail_server = "smtp.exmail.qq.com"
    sender = 'yuyang@forwardx.com'
    sender_password = 'AcgB5ZvhEsZNrYaf'
    receiver = email  # 收件人，多个收件人用逗号隔开

    # ③构造附件1
    att1 = MIMEText(open('../jira_remind/html_info/111.html', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="jira.html"'

    title = title
    mail = MIMEMultipart()
    mail['Subject'] = title
    mail['From'] = sender  # 发件人
    mail['To'] = receiver  # 收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
    mail.attach(body)
    mail.attach(att1)

    try:

        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_server, 25)  # 25 为 SMTP 端口号
        smtpObj.login(sender, sender_password)
        smtpObj.sendmail(sender, receiver.split(','), mail.as_string())
        smtpObj.quit()
    except BaseException as e:
        print(e)
        print('fail')
    else:
        print('success')


if __name__ == '__main__':
    info = f'Hi all:\n' \
           f'\n' \
           f'今日京东水饮流程稳定性测试完成：\n' \
           f'   开始时间（1)' \
           f'   :00）\n' \
           f'   结束时间（2）\n' \
           f'   共执行任务数量：2单\n' \
           f'   拣货点：2个\n' \
           f'   平均耗时：2分'
    runEmail_html('../jira_remind/html_info/111.html', '11111',
                  'yuyang@forwardx.com,yuyang110221@126.com,1149273360@qq.com')

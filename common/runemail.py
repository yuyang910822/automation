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


def run_test():
    # 定义测试用例路径

    # 存放报告的文件夹
    report_dir = '../report'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern="test21.py", top_level_dir=None)
    # 报告命名时间格式化
    now = time.strftime("%Y-%m-%d %H~%M~%S")
    # 报告文件完整路径
    report_name = report_dir + '/' + now + 'result.html'
    with open(report_name, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title=' 测试结果如下：', description='用例执行情况：')
        # 执行测试用例文件
        runner.run(discover)


def runEmail(file, title):
    """
    Email发送
    :return:
    """
    # file = open(file, 'rb')
    # file_data = str(file.read())
    # file.close()
    # print(file_data)
    print(file)
    body = MIMEText(file, 'plain', 'utf8')

    # 构造邮件主体
    mail_server = "smtp.exmail.qq.com"
    sender = 'yuyang@forwardx.com'
    sender_password = 'AcgB5ZvhEsZNrYaf'
    receiver = 'yuyang110221@126.com,yuyang@forwardx.com'  # 收件人，多个收件人用逗号隔开

    title = title
    mail = MIMEMultipart()
    mail['Subject'] = title
    mail['From'] = sender  # 发件人
    mail['To'] = receiver  # 收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
    mail.attach(body)

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
    runEmail(info,'11111')


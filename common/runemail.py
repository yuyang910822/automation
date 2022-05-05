import os
import smtplib
import time
import unittest

import HTMLTestRunner
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from base.base import Main
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
    with open(report_name, 'wb')as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title=' 测试结果如下：', description='用例执行情况：')
        # 执行测试用例文件
        runner.run(discover)

def runEmail():
    """
    Email发送
    :return:
    """

    target_dir = os.path.join(report_dir, os.listdir(report_dir)[-1])

    # 构建HTML文本
    file = open(target_dir, 'rb')
    file_data = str(file.read())
    file.close()
    print(file_data)
    body = MIMEText(file_data, 'html', 'utf8')


    # 构造图片正文
    # file = open("../png/1.png", 'rb').read()
    # png = MIMEImage(file)
    # png.add_header('Content-ID', "<image1>")
    # png["Content-Disposition"] = 'attachment; filename="testimage.png"'
    # 构造附件

    html = MIMEApplication(open(target_dir, 'rb').read())
    html.add_header('Content-Disposition', 'attachment', filename='测试报告.html')

    # 构造邮件主体
    mail_server = "smtp.office365.com"
    sender = 'yuyang@forwardx.com'
    sender_password = 'Yy123123'
    receiver = 'yuyang110221@126.com,yuyang@forwardx.com'  # 收件人，多个收件人用逗号隔开
    date = Main().getDate()
    title = ''.join(['【集群系统', str(date)])+"】--测试报告"
    mail = MIMEMultipart()
    mail['Subject'] = title
    mail['From'] = sender  # 发件人
    mail['To'] = receiver  # 收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
    mail.attach(body)
    # mail.attach(png)
    mail.attach(html)
    try:
        smtp = smtplib.SMTP(mail_server, port=587)  # 连接邮箱服务器
        smtp.starttls()
        smtp.login(sender, sender_password)  # 登录邮箱
        smtp.sendmail(sender, receiver.split(','), mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
        smtp.quit()  # 发送完毕后退出smtp
    except:
        print('fail')
    else:
        print('success')


if __name__ == '__main__':
    # runtest()
    runEmail()

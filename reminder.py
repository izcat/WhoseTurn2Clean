import os
from datetime import datetime
import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText
from emailsInfo import *

ids = [item['id'] for item in allInfo]
names = [item['name'] for item in allInfo]
emails = [item['email'] for item in allInfo]
id_index = {allInfo[o]['id']:o for o in range(len(allInfo))}


emailKey = 'xxxxxxx'
# 如果检测到程序在 Github Actions 内运行，那么读取环境变量中的邮箱密码
# 在 Actions secrets中设置 EMAIL_KEY
if os.environ.get('GITHUB_RUN_ID', None):
	emailKey = os.environ.get('EMAIL_KEY', '') 
	print('emailKey:', emailKey)

# 今天值日编号
def calOrder(tot, yesterdayId=''):
	yesterdayOrder = id_index.get(yesterdayId, '')

	# 没有昨日编号 自动推算
	# 2021-10-8 id:4, order:3
	if yesterdayOrder == '':
		day0 = datetime(2021, 10, 8)
		today = datetime.now()
		passDays = (today - day0).days
		index = (3 + passDays) % tot
	else:
		index = (yesterdayOrder+1) % tot

	return index

def sendEmail(sender, mail_passwd, receiver, subject, msg):
    try:
        body = MIMEText(str(msg), 'plain', 'utf-8')
        body['From'] = formataddr(["notifier", sender])
        body['To'] = formataddr(["me", receiver])
        body['Subject'] = subject

        smtp_port = 465 # or 587
        smtp_server = "smtp.sina.com"
	
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp.login(sender, mail_passwd)
        smtp.sendmail(sender, receiver, body.as_string())
        smtp.quit()
        print("邮件发送成功")
    except Exception as ex:
        print("邮件发送失败")
        print(ex)
	
def sendMsg(index):
	idReminded = ids[index]
	nameReminded = names[index]
	emailReminded = emails[index]

	msgEmail = "【饮茶小助手提示您】：今日卫生值班是%d号%s" % (idReminded, nameReminded)

	print(nameReminded, emailReminded, emailKey, msgEmail)
	sendEmail('zongeek@sina.com', emailKey, emailReminded,
		  '【832睡眠体验研究中心重要通知】', msgEmail)


def readFile():
	with open('yesterday.dat', 'r') as f:
		content = f.read()
		try:
			yesterdayId = int(content)
			if yesterdayId in ids:
				return yesterdayId
		except Exception as e:
			print("readFile error:")			
			print(e)

	return ''

def saveFile(id):
	with open('yesterday.dat', 'w') as f:
		f.write(str(id))


def autoRun():
	yesterdayId = readFile()
	index = calOrder(12, yesterdayId)
	print(index, names[index])
	
	# 发送邮件提醒
	sendMsg(index)
	with open('message.txt', 'w') as f:
		f.write("【饮茶小助手提示您】：今日卫生值班是%d号%s" % (ids[index], names[index]))
	with open('mail.txt', 'w') as f:
		f.write(emails[index])
	
	# 保存今天信息
	saveFile(ids[index])

if __name__ == '__main__':
	autoRun()

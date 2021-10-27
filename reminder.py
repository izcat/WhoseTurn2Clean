import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from emailsInfo import *

ids = [item['id'] for item in allInfo]
names = [item['name'] for item in allInfo]
emails = [item['email'] for item in allInfo]
id_index = {allInfo[o]['id']:o for o in range(len(allInfo))}

duties = ["套间清扫，拖地",
		"洗手台清理，套间桌子清洁",
		"卫生间垃圾扫除，洁厕灵清理",
		"更换卫生间垃圾袋，卫生间和套间垃圾桶清洗",
		"套间清扫，拖地",
		"洗手台清理，套间桌子清洁",
		"卫生间垃圾扫除，洁厕灵清理",
		"更换卫生间垃圾袋，卫生间和套间垃圾桶清洗",
		"套间清扫，拖地",
		"洗手台清理，套间桌子清洁",
		"卫生间垃圾扫除，洁厕灵清理",
		"更换卫生间垃圾袋，卫生间和套间垃圾桶清洗"]
duties = ["拖浴室、拖卫生间、更换套间垃圾袋、换水；"+item for item in duties]

emailKey = 'xxxxxxx'
wechatKey = ''
# 如果检测到程序在 Github Actions 内运行，那么读取环境变量中的邮箱密码
# 在 Actions secrets中设置 EMAIL_KEY
if os.environ.get('GITHUB_RUN_ID', None):
	emailKey = os.environ.get('EMAIL_KEY', '') 
	wechatKey = os.environ.get('WECHAT_KEY', '') 
	# print('emailKey:', emailKey)

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
        body['From'] = sender
        body['To'] = receiver
        body['Subject'] = subject

        smtp_port = 465 # or 587
        smtp_server = "smtp.qq.com"
	
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp.login(sender, mail_passwd)
        smtp.sendmail(sender, receiver, body.as_string())
        smtp.quit()
        print("邮件发送成功")
    except Exception as ex:
        print("邮件发送失败")
        print(ex)
	
        # 微信通知发送失败
        import requests
        msg_url = "https://sctapi.ftqq.com/{}.send?text={}&desp={}".format(wechatKey, '今日值日提醒失败', repr(ex))
        requests.get(msg_url)
	
def sendMsg(index):
	idReminded = ids[index]
	nameReminded = names[index]
	emailReminded = emails[index]

	msgEmail = "【饮茶小助手提示您】：今日卫生值班是%d号%s" % (idReminded, nameReminded)
	msgEmail += "\n【今日值日任务清单】：" + duties[index]

	print(nameReminded, emailReminded, emailKey, msgEmail)
	sendEmail('zongyc@foxmail.com', emailKey, emailReminded,
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
# 	with open('message.txt', 'w') as f:
# 		f.write("【饮茶小助手提示您】：今日卫生值班是%d号%s" % (ids[index], names[index]))
# 	with open('mail.txt', 'w') as f:
# 		f.write(emails[index])
	
	# 保存今天信息
	# 无法直接保存仓库文件
	# 因此 readFile 内容一直为空 待改进
	# saveFile(ids[index])

if __name__ == '__main__':
	autoRun()

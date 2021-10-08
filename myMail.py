import smtplib
from email.mime.text import MIMEText

class Mail:
	# 邮箱服务器地址
	mailServer = 'smtp.sina.com'

	def __init__(self):
		self.mail = None

	def send(self, Send, Recv, password, mailMsg, mailSub=''):
		self.mail = MIMEText(mailMsg)
		self.mail['Subject'] = mailSub
		self.mail['From'] = Send
		self.mail['To'] = Recv

		try:
			smtp = smtplib.SMTP(Mail.mailServer, port=25)
			smtp.login(Send, password)
			smtp.sendmail(Send, Recv, self.mail.as_string())
			smtp.quit()
			print("ok")
		except Exception as e:
			print(e)
			print("not ok")

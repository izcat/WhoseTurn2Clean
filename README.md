# WhoseTurn2Clean

今天轮到哪位帅哥来打扫832寝室？


- 每日提醒时间
  北京时间 10:24 AM (UTC 2:24)



## 自动运行原理

Github Actions 提供了CI/CD环境，配置好 `.github/workflows`下的 `*.yml`文件后，自动执行工作流。

- 工作流触发

  设置工作流触发条件为 `schedule cron: 24 2 * * *`，表示每天在UTC时间 2:24分，即北京时间 10:24 AM 启动工作流。

- 工作流任务

  运行环境选择 ubuntu 服务器及 python 3.6

  使用 `python ./reminder.py` 执行代码



## 代码运行过程

![image](https://user-images.githubusercontent.com/32667939/136580720-8bd2f0ee-a689-4490-a53a-0622afd2af03.png)


## 踩坑记录
- secrets 设置  
  依次点击 Settings => Secrets => New repository secret  
  填好 Name: YOUR_SECRET_NAME 和 Value  
  务必在 `*.yml` 文件中的运行环境添加获取 secret  
  ```
  env:
      SECRET_VALUE: ${{secrets.YOUR_SECRET_NAME}}
  ```
  在运行代码中，使用以下代码拿到设置的 Value  
  ```
  if os.environ.get('GITHUB_RUN_ID', None):
	    SECRET_KEY = os.environ.get('SECRET_VALUE', '') 
  ```
- 邮件发送  
  `smtplib.SMTP` 发送邮件可能会被 Github拦截，后台显示已发送，但接收人收不到邮件  
  解决：
  使用 `smtplib.SMTP_SSL` 加密方式发送，注意端口号修改为 465，根据不同邮箱服务器说明进行设置
---

（完）

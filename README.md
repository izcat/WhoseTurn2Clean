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

---

（完）

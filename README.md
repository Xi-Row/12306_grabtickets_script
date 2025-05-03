# 12306抢票脚本
---


## Introduction  
---
基于Python Selenium库 apscheduler库 和 web Crawler 编写的python脚本实现定时、自动化、高效的12306抢票脚本，多次实测，网络良好，CPU性能一般的情况下平均购票用时2.86s。


## Basic config and Operation
---
1. 下载chromedriver 浏览器驱动器(与浏览器版本相对应) [下载地址]([Chrome for Testing availability](https://googlechromelabs.github.io/chrome-for-testing/))
	并将其添加到chromedriver目录下，再将其绝对路径添加到config/setting.py中
	
2. 下载必要依赖
所用必要依赖已经整理到requests.txt中，在命令行(终端)中输入：
```
pip install -r requests.txt
```
3. 运行脚本(建议在pycharm中运行)
* Pycharm:
	* 执行setting.py 获取车站代号填入setting.py中并填写必要信息
	* 执行execute.py开始购票

* Windows
	* 打开./data/station_code.xlsxh查询对应的车站代号
	* 进入项目根目录目录，执行程序
	```
	python .\grab_ticket\excute.py
	```


## Demo
---
NO

## Attention
---
	1. 如果一票难求，s可提前10~20 s设置购票时间  
	2. PAY_TIME_LEFT 决定是否留时间在浏览器上付款
	3. 可一次性多人(包含在12306乘车人列表中)购票并分开选择座位类别
	4. 可选学生票(12306只能为自己购买学生票)
	5. 可为单人选座位号(前提是票足够)
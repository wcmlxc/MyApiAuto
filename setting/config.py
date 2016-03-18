#!/usr/bin/env python
# -*- coding:utf-8 -*-

# jp jsonSchema

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

############################################################################################
#区分是否按模块执行，True为按模块执行，False为不按模块执行
#	如果为True，一定要配置数组toRunList,如：toRunList = ["登录","注册"]
#	如果为False，会按顺序全部执行
#注意：True/False 一定要注意大小写，其类型为布尔值
############################################################################################
isChooseList = True
toRunList = ["登录","注册","确认订单"]

############################################################################################
#commonParam 为公共参数,需要在这里配置，每个接口都会使用这些参数
#
#	注意： 	公共参数sign不用在这里写，程序会自动加上sign
#			第一次创建数据库表的时候会插入一条记录在businessTools.createBasicTable中,
#			所以此处字段只能增加，不能减少，需要优化businessTools.createBasicTable方法		
############################################################################################
commonParam = ["app_client_id","app_version","sid"]

############################################################################################
#
#mailto_list 为邮件列表
#
############################################################################################
#mailto_list=["zhoudongbin@mmbang.net","xierong@mmbang.net","shiyanping@mmbang.net"]
mailto_list=["zhoudongbin@mmbang.net"]

#获取main.py入口程序的目录的上级目录，也就是根目录
#path = os.path.abspath(sys.argv[0])
path = os.getcwd()
rootPath = os.path.dirname(path)
#区分不同系统对文件路径进行处理
#根目录
#rootPath = r"C:\Users\zhoudonbin\Desktop\APIAuto"
if os.name == "nt":
	#Windows系统。。。。
	#一级目录
	apiPath = rootPath + r"\api"
	flowPath = rootPath + r"\flow"
	schemaPath = rootPath + r"\schema"
	toolsPath = rootPath + r"\tools"
	resultPath = rootPath + r"\result"
	settingPath = rootPath + r"\setting"
	testPath = rootPath + r"\test"
	logPath = rootPath + r"\log"

	#二级目录:result
	databasePath = resultPath + r"\database"
	reportDirPath = resultPath + r"\report"

	#文件目录
	databaseFilePath = databasePath + r"\database.db"
	reportFilePath = reportDirPath + r"\index.html"
	reportFileDemoPath = reportDirPath + r"\indexDemo.html"
	logFilePath = logPath + r"\softwareLog.log"
	apiTestCaseFilePath = testPath + r"\apiTestCase.xlsx"
elif os.name == "posix":
	#Mac/Linux系统。。。。
	#一级目录
	apiPath = rootPath + r"/api"
	flowPath = rootPath + r"/flow"
	schemaPath = rootPath + r"/schema"
	toolsPath = rootPath + r"/tools"
	resultPath = rootPath + r"/result"
	settingPath = rootPath + r"/setting"
	testPath = rootPath + r"/test"
	logPath = rootPath + r"/log"

	#二级目录:result
	databasePath = resultPath + r"/database"
	reportDirPath = resultPath + r"/report"

	#文件目录
	databaseFilePath = databasePath + r"/database.db"
	reportFilePath = reportDirPath + r"/index.html"
	reportFileDemoPath = reportDirPath + r"/indexDemo.html"
	logFilePath = logPath + r"/softwareLog.log"
	apiTestCaseFilePath = testPath + r"/apiTestCase.xlsx"
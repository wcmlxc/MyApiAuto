#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
os.chdir(os.path.dirname(sys.argv[0]))
print os.getcwd()
sys.path.append("../setting")
sys.path.append("../business")
sys.path.append("../tools")
import json
import config
import jsonpath
from readExcel import readExcel
from requestApi import requestApi
import businessTools
from dataCenter import dataCenter
import reportGenerate
import beautifulSoup
import mainFlow

#设置测试用例地址以及构建次数
apiTestCaseFilePath = config.apiTestCaseFilePath
# print apiTestCaseFilePath

#删除日志文件
if os.path.exists(config.logFilePath):
	os.remove(config.logFilePath)

#设置构建次数
currentBuildTimes = businessTools.fetchData("select distinct buildTimes from result order by buildTimes desc limit 1")
if isinstance(currentBuildTimes, int):
	buildTimes = currentBuildTimes + 1
else:
	buildTimes = 1

#执行setUp
mainFlow.setUp()

#################################################
#根据config.isChooseList的值来选择不同的执行模式
#	True:执行config文件中toRunList中的sheet模块
#	False:按顺序执行所有的sheet模块
#################################################
if config.isChooseList is True:
	excel = readExcel(apiTestCaseFilePath)
	for sheet in config.toRunList:
		excel.setTableSheet_by_name(sheet)
		for rowNum in xrange(1, excel.getRows()):
			mainFlow.requestExcel(apiTestCaseFilePath,sheet,rowNum,buildTimes)
elif config.isChooseList is False:
	excel = readExcel(apiTestCaseFilePath)
	allSheets = excel.getSheetCount()
	for sheet in xrange(1, allSheets):
		excel.setTableSheet(sheet)
		for rowNum in xrange(1, excel.getRows()):
			mainFlow.requestExcel(apiTestCaseFilePath,sheet,rowNum,buildTimes)

#执行tearDown
mainFlow.tearDown()

#python渲染html模板
beautifulSoup.main()

#发送邮件
#reportGenerate.main()
# http://haowan.mmbang.com/item/default/view?_from_=search&item_id=13516&app_client_id=4&app_version=1.4.0&sid=9e8130966be17539f0cce15075ace455&sign=202d8b4482c15cb38c00360594c832cb
# http://haowan.mmbang.com/item/default/view?_from_=search&app_client_id=1&app_version=1.4.0&channel=AppStore&device_id=f59f16f4da31a9ca5c90aa013bab0f2444147ab0&id=13515&isGetMore=0&lat=31.19957&lng=121.5823&os_version=8.4&screen_height=1334&screen_width=750&sid=2fd21638558a412f77db0d3bd87af5cc&sign=309b05b70dee8b692b570229b263d00a&time=1458291080.751800
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

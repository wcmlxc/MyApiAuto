#!/usr/bin/env python
# -*- coding:utf-8 -*-

# jp jsonSchema

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../setting")
sys.path.append("../tools")
sys.path.append("../business")
import os
import config
import jsonpath
from readExcel import readExcel
import re
import json
import businessTools
import utils
# 设置测试用例路径
apiTestCaseFilePath = config.apiTestCaseFilePath

class dataCenter(object):
	"""docstring for dataCenter"""

	def __init__(self, apiTestCaseFilePath, sheet, rowNum):#rowNum为行数
		super(dataCenter, self).__init__		
		# 建立excel实例
		utils.logSave("开始创建excel实例")
		self.excel = readExcel(apiTestCaseFilePath)
		utils.logSave("结束创建excel实例")
		
		if config.isChooseList is True:
			self.excel.setTableSheet_by_name(sheet)
		elif config.isChooseList is False:
			self.excel.setTableSheet(sheet)

		utils.logSave("开始创建属性")

		self.rowNum = rowNum
		self.testCaseNumber = businessTools.dataProcess(self.excel.read(rowNum+1,1),float,0)
		self.testCaseModule = businessTools.dataProcess(self.excel.read(rowNum+1,2),str,"")
		self.testCaseName = businessTools.dataProcess(self.excel.read(rowNum+1,3),str,"")
		self.apiName = businessTools.dataProcess(self.excel.read(rowNum+1,4),str,"")
		self.apiNotice = businessTools.dataProcess(self.excel.read(rowNum+1,5),str,"")
		self.testCaseLevel = businessTools.dataProcess(self.excel.read(rowNum+1,6),str,"P99")
		self.method = businessTools.dataProcess(self.excel.read(rowNum+1,7),str,"get").lower()
		self.host = businessTools.dataProcess(self.excel.read(rowNum+1,8),str,"")
		self.url = businessTools.dataProcess(self.excel.read(rowNum+1,9),str,"")
		self.fullurl = self.host + self.url
		self.data = businessTools.dataProcess(self.excel.read(rowNum+1,10),str,"")
		self.passObject = businessTools.dataProcess(self.excel.read(rowNum+1,11),str,"")		
		self.checkData = businessTools.dataProcess(self.excel.read(rowNum+1,12),str,"")
		self.checkMode = businessTools.dataProcess(self.excel.read(rowNum+1,13),str,"noMode")
		self.isNeedToRun = businessTools.dataProcess(self.excel.read(rowNum+1,14),str,"no").lower()
		self.sleepTime = businessTools.dataProcess(self.excel.read(rowNum+1,15),float,0)
		self.dependency = businessTools.dataProcess(self.excel.read(rowNum+1,16),str,"")
		#self.dependency = ""
		
		if self.isNeedToRun == "yes":
			# 进行参数透传的嵌套循环处理
			self.fullurl = businessTools.replaceString(self.fullurl)
			self.data = businessTools.replaceString(self.data)
			self.checkData = businessTools.replaceString(self.checkData)
			utils.logSave("透传处理得到的data为:" + self.data + "类型：" + str(type(self.data)))
			utils.logSave("透传处理得到的checkData为:" + self.checkData + "类型：" + str(type(self.checkData)))
			utils.logSave("透传处理得到的fullurl为:" + self.fullurl)

			# Update公共参数表

			# 导入公共参数
			if isinstance(self.data, unicode):
				self.data = self.data.encode('utf-8')
			if isinstance(self.data, str):
				self.skipList = []
				for param in config.commonParam:
					if re.search('^' + param + '\=',self.data) or re.search('\&' + param + '\=',self.data) or re.search('\"' + param + '\"\:',self.data):
						self.skipList.append(param)
				utils.logSave("skipList:" + str(self.skipList))
				# self.skipList = ["app_client_id"]
				utils.logSave("self.data:" + str(self.data))
				self.data = businessTools.dataPlus(self.data, config.commonParam, self.skipList)
				self.data = businessTools.dataPlus(self.data, {"sid":""})
				businessTools.getSign(self.data)
				self.data = businessTools.dataPlus(self.data, {"sign":""})
		else:
			utils.logSave("isNeedToRun为" + self.isNeedToRun + " ，不需要执行")

		# 以下为需要转化为dict类型的字段
		# self.data = self.stringToDict(self.data)
		# self.passObject = self.stringToDict(self.passObject)
		self.checkData = self.stringToDict(self.checkData)
		self.dependency = self.stringToDict(self.dependency)

		utils.logSave("testCaseNumber:" + str(self.testCaseNumber))
		utils.logSave("fullurl为:" + self.fullurl)
		utils.logSave("isNeedToRun为:" + self.isNeedToRun)
		utils.logSave("sleepTime:" + str(self.sleepTime))
		utils.logSave("checkData:" + str(self.checkData))
		utils.logSave("dependency:" + str(self.dependency))
		print "数据处理中心处理得到的数据类型data:{}passObject:{}checkMode{}".format(type(self.data),type(self.passObject),type(self.checkMode))

	def stringToDict(self, mystring):
		utils.logSave("stringToDict输入参数：" + str(mystring) + "类型：" + str(type(mystring)))
		if isinstance(mystring,str) and mystring is not "":
			if re.search('^{.*}$',mystring):
				try:
					return json.loads(mystring)
				except Exception, e:
					utils.logSave("stringToDict()出现异常，入参为：" + str(mystring) + e)
		utils.logSave("stringToDict不满足匹配条件，返回原输入参数")
		return mystring

if __name__ == '__main__':
	apiTestCaseFilePath = config.apiTestCaseFilePath
	dc = dataCenter(apiTestCaseFilePath, "注册", 2)
	print dc.testCaseNumber
	dc.testCaseNumber = 3
	print dc.testCaseNumber
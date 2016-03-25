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
	"""docstring for dataCenter"""()

	def __init__(self, apiTestCaseFilePath, sheet, rowNum):#rowNum为行数
		super(dataCenter, self).__init__		#读取每条case的各个字段并分别赋值
		# 建立excel实例
		self.excel = readExcel(apiTestCaseFilePath)
		if config.isChooseList is True:
			self.excel.setTableSheet_by_name(sheet)
		elif config.isChooseList is False:
			self.excel.setTableSheet(sheet)
			
		self.rowNum = rowNum
		self.testCaseNumber = int(self.excel.read(rowNum+1,1))
		self.testCaseModule = str(self.excel.read(rowNum+1,2)).replace(" ","")
		self.testCaseName = str(self.excel.read(rowNum+1,3)).replace(" ","")
		self.apiName = str(self.excel.read(rowNum+1,4)).replace(" ","")
		self.apiNotice = str(self.excel.read(rowNum+1,5)).replace(" ","")
		self.testCaseLevel = str(self.excel.read(rowNum+1,6)).replace(" ","")
		self.method = str(self.excel.read(rowNum+1,7)).lower().replace(" ","")
		self.host = str(self.excel.read(rowNum+1,8)).replace(" ","")
		self.url = str(self.excel.read(rowNum+1,9)).replace(" ","")
		self.data = self.excel.read(rowNum+1,10).encode("utf-8").replace(" ","")
		self.passObject = self.excel.read(rowNum+1,11).encode("utf-8").replace(" ","")
		self.checkData = self.excel.read(rowNum+1,12).encode("utf-8").replace(" ","")
		self.checkMode = str(self.excel.read(rowNum+1,13)).replace(" ","").replace(" ","")
		self.isNeedToRun = str(self.excel.read(rowNum+1,14)).lower().replace(" ","")
		# self.dependency = str(self.excel.read(rowNum+1,15)).encode("utf-8")

		# print "dependency:" + self.dependency
		self.fullurl = self.host + self.url
		utils.logSave("fullurl为:" + self.fullurl)
		utils.logSave("isNeedToRun为:" + self.isNeedToRun)

		if self.isNeedToRun == "yes":
			# 进行参数透传的嵌套循环处理
			self.fullurl = businessTools.replaceString(self.fullurl)
			self.data = businessTools.replaceString(self.data)
			self.checkData = businessTools.replaceString(self.checkData)
			utils.logSave("透传处理得到的fullurl为:" + self.fullurl)

			# Update公共参数表

			# 导入公共参数
			if isinstance(self.data, unicode):
				self.data = self.data.encode()
			if isinstance(self.data, str):
				self.skipList = []
				for param in config.commonParam:
					if re.search('^' + param + '\=',self.data) or re.search('\&' + param + '\=',self.data) or re.search('\"' + param + '\"\:',self.data):
						self.skipList.append(param)
				utils.logSave("skipList:" + str(self.skipList))
				# self.skipList = ["app_client_id"]
				self.data = businessTools.dataPlus(self.data, config.commonParam, self.skipList)
				self.data = businessTools.dataPlus(self.data, {"sid":""})
				businessTools.getSign(self.data)
				self.data = businessTools.dataPlus(self.data, {"sign":""})
		else:
			utils.logSave("isNeedToRun为" + self.isNeedToRun + " ，不需要执行")

		
		print "数据处理中心处理得到的数据类型data:{}passObject:{}checkMode{}".format(type(self.data),type(self.passObject),type(self.checkMode))

if __name__ == '__main__':
	apiTestCaseFilePath = config.apiTestCaseFilePath
	dc = dataCenter(apiTestCaseFilePath, "注册", 2)
	print dc.testCaseNumber
	dc.testCaseNumber = 3
	print dc.testCaseNumber
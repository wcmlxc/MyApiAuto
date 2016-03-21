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
# 设置测试用例路径
apiTestCaseFilePath = config.apiTestCaseFilePath

class dataCenter(object):
	"""docstring for dataCenter"""
	def __init__(self, apiTestCaseFilePath, sheet, rowNum):#rowNum为行数
		super(dataCenter, self).__init__()
		#读取每条case的各个字段并分别赋值
		# 建立excel实例
		print 111111111111111111111
		self.excel = readExcel(apiTestCaseFilePath)
		if config.isChooseList is True:
			self.excel.setTableSheet_by_name(sheet)
		elif config.isChooseList is False:
			self.excel.setTableSheet(sheet)
			
		self.rowNum = rowNum
		self.testCaseNumber = int(self.excel.read(rowNum+1,1))
		self.testCaseModule = str(self.excel.read(rowNum+1,2))
		self.testCaseName = str(self.excel.read(rowNum+1,3))
		self.apiName = str(self.excel.read(rowNum+1,4))
		self.apiNotice = str(self.excel.read(rowNum+1,5))
		self.testCaseLevel = str(self.excel.read(rowNum+1,6))
		self.method = str(self.excel.read(rowNum+1,7)).lower()
		self.host = str(self.excel.read(rowNum+1,8))
		self.url = str(self.excel.read(rowNum+1,9))
		self.data = self.excel.read(rowNum+1,10).encode("utf-8")
		self.passObject = self.excel.read(rowNum+1,11).encode("utf-8")
		self.checkData = self.excel.read(rowNum+1,12).encode("utf-8")
		self.checkMode = str(self.excel.read(rowNum+1,13)).replace(" ","")
		self.isNeedToRun = str(self.excel.read(rowNum+1,14)).lower().replace(" ","")

		self.fullurl = self.host + self.url
		print self.host + self.url
		print self.isNeedToRun
		if self.isNeedToRun == "yes":
			# 拼接url
			print "数据处理中心处理得到的fullurl:{}".format(self.fullurl)
			# 进行参数透传的嵌套循环处理
			self.fullurl = businessTools.replaceString(self.fullurl)
			self.data = businessTools.replaceString(self.data)
			self.checkData = businessTools.replaceString(self.checkData)
			print "数据处理中心处理得到的fullurl:{}".format(self.fullurl)
			# 导入公共参数
			if isinstance(self.data, unicode):
				self.data = self.data.encode()
			self.data = businessTools.dataPlus(self.data,config.commonParam)
			businessTools.getSign(self.data)
			self.data = businessTools.dataPlus(self.data,["sign"])
		elif self.isNeedToRun == "no":
			pass

		
		print "数据处理中心处理得到的数据类型data:{}passObject:{}checkMode{}".format(type(self.data),type(self.passObject),type(self.checkMode))

if __name__ == '__main__':
	apiTestCaseFilePath = config.apiTestCaseFilePath
	dc = dataCenter(apiTestCaseFilePath, "注册", 2)
	print dc.testCaseNumber
	dc.testCaseNumber = 3
	print dc.testCaseNumber
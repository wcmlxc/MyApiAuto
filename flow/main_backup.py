#!/usr/bin/env python
# -*- coding:utf-8 -*-

# jp jsonSchema
import sys
import re
sys.path.append("../business")
sys.path.append("../tools")
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../setting")
import json
import config
import jsonpath
from readExcel import readExcel
from requestApi import requestApi
import businessTools
from dataCenter import dataCenter
import reportGenerate
import beautifulSoup

#============================================SETUP 开始：建立数据库表，建立基本请求参数表，删除基本请求参数表中sign和sid=========================================
# 设置测试用例路径
apiTestCaseFilePath = config.apiTestCaseFilePath

# 设置第几次构建
buildTimes = 3

# 建立数据库表result和basic（如果没有的话）
businessTools.creatResultTable()
businessTools.createBasicTable()
#删除sign和sid数据
businessTools.updateSign("")
businessTools.updateSid("")
#============================================SETUP 结束 ========================================================================================================

# 建立excel实例
excel = readExcel(apiTestCaseFilePath)

# 获取excel的所有sheet数量
allSheets = excel.getSheetCount()

# 循环对每个sheet进行操作
for sheetNum in xrange(1, allSheets):
# 读取用例excel的第y个sheet
	excel.setTableSheet(sheetNum)

	# 循环对每个sheet的每条用例进行请求操作
	for rowNum in xrange(1, excel.getRows()):
		#读取每条case的各个字段并分别赋值
		print('#'*50 + "开始执行用例：SHEET{};CASE{}" + '#'*50).format(sheetNum,rowNum)
		testCaseNumber = int(excel.read(rowNum+1,1))
		testCaseModule = str(excel.read(rowNum+1,2))
		testCaseName = str(excel.read(rowNum+1,3))
		testCaseLevel = str(excel.read(rowNum+1,4))
		method = str(excel.read(rowNum+1,5)).lower()
		host = str(excel.read(rowNum+1,6))
		url = str(excel.read(rowNum+1,7))
		data = excel.read(rowNum+1,8).encode("utf-8")
		passObject = excel.read(rowNum+1,9).encode("utf-8")
		checkData = excel.read(rowNum+1,10)
		checkMode = excel.read(rowNum+1,11)
		apiDescription = excel.read(rowNum+1,12)
		apiNotice = excel.read(rowNum+1,13)

		#拼接url
		fullurl = host + url

		# dc = dataCenter(rowNum)
		# testCaseNumber = dc.testCaseNumber
		# testCaseName = dc.testCaseName
		# testCaseLevel = dc.testCaseLevel
		# method = dc.method
		# host = dc.host
		# url = dc.url
		# data = dc.data
		# passObject = dc.passObject
		# checkData = dc.checkData
		# checkMode = dc.checkMode
		# apiDescription = dc.apiDescription
		# apiNotice = dc.apiNotice


		data = businessTools.dataPlus(data,["app_client","app_version","sid"])
		# print "第一次拼接以后得到的data:{}".format(data)
		businessTools.getSign(data)
		data = businessTools.dataPlus(data,["sign"])


		#创建request连接的实例
		req = requestApi(fullurl,data)

		#执行请求操作
		if method == "get":
			print "请求方式为get,执行get方法"
			req.get()
		elif method == "post":
			print "请求方式为post,执行post方法"
			req.post()

		#打印完整URL
		print "请求的完整URL:{}".format(req.getUrl())

		#获取json返回，作比对
		res = req.getJson()
		print "获取到的response:{}".format(res)

		# ================================透传参数处理====================================================
		print "透传参数处理开始..."
		print "透传参数打印:{}".format(passObject)+"--类型:{}".format(type(passObject))
		if passObject is None or passObject is "":
			# 透传参数为空时，参数的值也为空
			print "透传参数为空..."
			passObjectValue = ""
		elif passObject == "sid":
			# 透传参数设置为sid时，获取sid的值保存到公共参数表的sid字段中
			print "透传参数为sid..."
			sidValue = businessTools.returnValue(res, "sid")
			businessTools.updateSid(sidValue)
			passObjectValue = sidValue
			print "sid:{}".format(sidValue)
		else:
			# 透传参数为其他值时，获取透传参数的值保存到结果表中
			print "透传参数为其他值（非sid）..."
			try:
				passObjectValue = businessTools.returnValue(res, passObject)
			except Exception, e:
				print e
				passObjectValue = passObject

		print "passObjectValue:{}".format(passObjectValue)
		print "透传参数处理结束"
		# ================================透传参数处理结束==================================================

		# ================================断言===============================================================
		try:
			#判断不同的校验模式，做不同的处理
			if checkMode == "exact":
				#精确匹配模式
				print "进入exact模式"
				print "打印excel里面的字典:{}".format(checkData)

				if checkData is not None or checkData is not  "":
					checkData = json.loads(checkData)
				result = cmp(res,checkData) #完全匹配返回0；第一个参数<第二个参数，返回-1；第一个参数>第二个参数，返回1

			elif checkMode.startswith("jsonpath"):
				#jsonpath匹配模式
				print "进入jsonpath模式"
				print "打印excel里面的字典:{}".format(checkData)

				if checkData is not None or checkData is not "":
					checkData = json.loads(checkData)

				for x in checkData:
					expression_data = x
					expression_result = checkData[x]

					#对数据进行处理，转化为list
					if isinstance(expression_result,list):
						r = []
						for x in xrange(0,len(expression_result)):
							expression_result[x] = unicode(expression_result[x])
							r.append(expression_result[x])
					# elif re.search('^pattern(.*)$',expression_result):
					# 	pattern = expression_result[8:-1]
					# 	re.search(pattern,)
					else:
						#加入一个临时数组r
						r = []
						r.append(expression_result)
					#获取jsonpath的值（为一个list）
					v = jsonpath.jsonpath(res, expression_data)

					print "EXCEL中数据转化得到的list结果:{}".format(r)
					print "JSONPATH获取到的结果:{}".format(v)
					result = cmp(r, v)#完全匹配返回0；第一个参数<第二个参数，返回-1；第一个参数>第二个参数，返回1
					if result is not 0:
						break
			else:
				#未定义时，返回99
				result = 99
			if checkMode.endswith("no"):
				if result == 0:
					result = 2
				elif result == 1 or result == -1:
					result = 0
		except Exception, e:
			print "断言异常，报错信息如下:{}".format(e)
			#程序异常结果返回98
			result = 98
		# ===============================================断言结束=========================================

		print "断言结果是:{}".format(result)
		responseTime = req.getResponseTime()
		statusCode = req.getStatusCode()

		# 把请求数据和请求结果录入数据库
		businessTools.insertTable(testCaseNumber,testCaseModule,testCaseName,testCaseLevel,apiDescription,apiNotice,method,host,url,str(
			data),passObject,passObjectValue,str(checkMode),result,responseTime,statusCode,buildTimes)
		#清空basic表中的sign值，防止影响后面的测试
		businessTools.updateSign("")
		print('#'*50 + "结束执行用例：SHEET{};CASE{}" + '#'*50).format(sheetNum,rowNum)
#==========================TEAR DOWN ,删除基本请求参数表中sign和sid字段========================================
businessTools.updateSign("")
businessTools.updateSid("")
#==========================TEAR DOWN ==========================================================================

#发送html/txt格式邮件，现在主要是html的
print "startSendEmail"
beautifulSoup.main()
#reportGenerate.main()
print "endSendEmail"

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
import utils
import json
import config
import jsonpath
from readExcel import readExcel
from requestApi import requestApi
import businessTools
from dataCenter import dataCenter
import reportGenerate
import beautifulSoup
import os

def setUp():
	# 建立数据库表result和basic（如果没有的话）
	businessTools.creatResultTable()
	businessTools.createBasicTable()
	#删除sign和sid数据
	businessTools.updateSign("")
	businessTools.updateSid("")
	
def tearDown():
	businessTools.updateSign("")
	businessTools.updateSid("")

# 循环对每个sheet的每条用例进行请求操作
# for rowNum in xrange(1, excel.getRows()):
def requestExcel(apiTestCaseFilePath, sheet, rowNum, buildTimes):
	utils.logSave('#'*10 + "开始执行用例--SHEET:" + str(sheet) + ";rowNum:" + str(rowNum) +'#'*10)

	#创建实例
	dc = dataCenter(apiTestCaseFilePath,sheet,rowNum)

	#判断是否执行
	if dc.isNeedToRun == "yes":
		utils.logSave("继续执行"*10)
	elif dc.isNeedToRun == "no":
		utils.logSave("不需要执行，跳过"*10)
		utils.logSave('#'*10 + "结束执行用例--SHEET:" + str(sheet) + ";rowNum:" + str(rowNum) +'#'*10)
		return 1

	# # 导入公共参数
	# dc.data = businessTools.dataPlus(dc.data,config.commonParam)
	# businessTools.getSign(dc.data)
	# dc.data = businessTools.dataPlus(dc.data,["sign"])

	if isinstance(dc.data,str):
	    if re.search('^{.*}$',dc.data):
	        dc.data = json.loads(dc.data)
	#创建request连接的实例
	dc.req = requestApi(dc.fullurl,dc.data)

	#执行请求操作
	if dc.method == "get":
		utils.logSave("请求方式为get,执行get方法")
		dc.req.get()
	elif dc.method == "post":
		utils.logSave("请求方式为post,执行post方法")
		dc.req.post()

	#打印完整URL
	utils.logSave("请求的完整URL:" + str(dc.req.getUrl()))
	#获取json返回
	dc.res = dc.req.getJson()
	utils.logSave("获取到的response:" + str(dc.res))

	# ================================透传参数处理====================================================
	utils.logSave("透传参数处理开始...")
	utils.logSave("透传参数打印:" + str(dc.passObject) + "类型:" + str(type(dc.passObject)))
	if dc.passObject is None or dc.passObject is "":
		# 透传参数为空时，参数的值也为空
		utils.logSave("透传参数为空...")
		dc.passObjectValue = ""
	elif dc.passObject == "sid":
		# 透传参数设置为sid时，获取sid的值保存到公共参数表的sid字段中
		utils.logSave("透传参数为sid...")
		dc.sidValue = businessTools.returnValue(dc.res, "sid")
		businessTools.updateSid(dc.sidValue)
		dc.passObjectValue = dc.sidValue
		utils.logSave("sid:" + str(dc.sidValue))
	else:
		# 透传参数为其他值时，获取透传参数的值保存到结果表中
		utils.logSave("透传参数为其他值（非sid）...")
		try:
			dc.passObjectValue = businessTools.returnValue(dc.res, dc.passObject)
		except Exception, e:
			utils.logSave(e,"error")
			dc.passObjectValue = dc.passObject
	utils.logSave("passObjectValue:" + str(dc.passObjectValue))
	utils.logSave("透传参数处理结束...")
	# ================================透传参数处理结束==================================================

	# ================================断言===============================================================
	try:
		#判断不同的校验模式，做不同的处理
		if dc.checkMode == "exact":
			#精确匹配模式
			utils.logSave("进入exact模式")
			utils.logSave("打印excel里面的字典:" + str(dc.checkData))
			if dc.checkData is not None or dc.checkData is not  "":
				dc.checkData = json.loads(dc.checkData)
			dc.result = cmp(dc.res,dc.checkData) #完全匹配返回0；第一个参数<第二个参数，返回-1；第一个参数>第二个参数，返回1

		elif dc.checkMode.startswith("jsonpath"):
			#jsonpath匹配模式
			utils.logSave("进入jsonpath模式")
			utils.logSave("打印excel里面的字典:" + str(dc.checkData))

			if dc.checkData is not None or dc.checkData is not "":
				dc.checkData = json.loads(dc.checkData)

			for x in dc.checkData:
				expression_data = x
				expression_result = dc.checkData[x]

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
				v = jsonpath.jsonpath(dc.res, expression_data)
				if v is False:
					dc.result = 4 #jsonpath没有找到结果
					break
				utils.logSave("EXCEL中数据转化得到的list结果:" + str(r))
				utils.logSave("JSONPATH获取到的结果:" + str(v))
				if utils.listContains(r,v):
					dc.result = 0
				else:
					dc.result = 3 #jsonpath结果不包含目标信息，返回3
				#dc.result = cmp(r, v)#完全匹配返回0；第一个参数<第二个参数，返回-1；第一个参数>第二个参数，返回1
				if dc.result is not 0:
					break
		else:	
			dc.result = 99 #chechkMode未定义错误，返回99

		if dc.checkMode.endswith("no"):
			if dc.result == 0:
				dc.result = 2 #jsonpathno模式下，结果不完全匹配
			elif dc.result == 1 or dc.result == -1 or dc.result == 3 or dc.result < 50:
				dc.result = 0
	except Exception, e:
		utils.logSave("断言异常，报错信息如下:" + str(e),"error")
		dc.result = 98 #程序异常结果返回98
	# ===============================================断言结束=========================================
	utils.logSave("断言结果是:" + str(dc.result))
	dc.responseTime = dc.req.getResponseTime()
	dc.statusCode = dc.req.getStatusCode()

	# 处理格式转换
	print("录入数据库的data:{}以及data的类型:{}").format(dc.data,type(dc.data))
	if isinstance(dc.data,dict):
		dc.data = json.dumps(dc.data)
	if isinstance(dc.passObject,dict):
		dc.passObject = json.dumps(dc.passObject)
	if isinstance(dc.passObjectValue,dict):
		dc.passObjectValue = json.dumps(dc.passObjectValue)
	if isinstance(dc.checkMode,dict):
		dc.checkMode = json.dumps(dc.checkMode)

	if dc.result == 0:
		dc.msg = ""
	else:
		dc.msg = jsonpath.jsonpath(dc.res, "$.[msg]")[0].encode().replace('\'','')
	utils.logSave("把请求数据和请求结果录入数据库")
	businessTools.insertTable(dc.testCaseNumber,dc.testCaseModule,dc.testCaseName,dc.apiName,dc.apiNotice,dc.testCaseLevel,dc.method,dc.host,dc.url,str(
		dc.data),dc.passObject,dc.passObjectValue,str(dc.checkMode),dc.result,dc.msg,dc.responseTime,dc.statusCode,buildTimes)
	utils.logSave("清空basic表中的sign值，防止影响后面的测试")
	businessTools.updateSign("")
	utils.logSave('#'*10 + "结束执行用例：SHEET-" + str(sheet) + ";CASE-" + str(rowNum) +'#'*10)
	return 0

if __name__ == '__main__':
	# 建立excel实例
	excel = readExcel(config.apiTestCaseFilePath)
	excel.setTableSheet(1)
	for rowNum in xrange(1, excel.getRows()):
		requestExcel(config.apiTestCaseFilePath,"登录",rowNum,3)
	print 1111

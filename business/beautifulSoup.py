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
from bs4 import BeautifulSoup
import utils
import config
import os
import businessTools

def main():
	utils.logSave("111")
	utils.logSave("渲染报告开始")
	reportFilePath = config.reportFilePath
	reportFileDemoPath = config.reportFileDemoPath

	dictTemp = {}

	totalApiCaseSql = "select Count(*) from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1)"
	totalApiCase = businessTools.fetchData(totalApiCaseSql)
	dictTemp["totalApiCase"] = totalApiCase

	totalApiSql = "select Count(distinct apiName) from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1)"
	totalApi = businessTools.fetchData(totalApiSql)
	dictTemp["totalApi"] = totalApi

	totalModuleSql = "select Count(distinct testCaseModule) from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1)"
	totalModule = businessTools.fetchData(totalModuleSql)
	dictTemp["totalModule"] = totalModule

	totalApiPassSql = "select Count(*) from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1) and result=0"
	totalApiPass = businessTools.fetchData(totalApiPassSql)
	dictTemp["totalApiPass"] = totalApiPass

	totalApiPassRate = utils.calPCT(totalApiPass,totalApiCase)
	dictTemp["totalApiPassRate"] = totalApiPassRate

	totalApiFail = totalApiCase - totalApiPass
	dictTemp["totalApiFail"] = totalApiFail

	totalApiFailRate = utils.calPCT(totalApiFail,totalApiCase)
	dictTemp["totalApiFailRate"] = totalApiFailRate

	totalAvgResTimeSql = "select Avg(responseTime) from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1)"
	totalAvgResTime = businessTools.fetchData(totalAvgResTimeSql)
	dictTemp["totalAvgResTime"] = totalAvgResTime

	totalResTimeOver1000Sql = "select Count(responseTime) from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1) and responseTime>1000"
	totalResTimeOver1000 = businessTools.fetchData(totalResTimeOver1000Sql)
	dictTemp["totalResTimeOver1000"] = totalResTimeOver1000

	totalStatusCodeErrorSql = "select Count(responseTime) from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1) and statusCode<>200"
	totalStatusCodeError = businessTools.fetchData(totalStatusCodeErrorSql)
	dictTemp["totalStatusCodeError"] = totalStatusCodeError


	totalStartTimeSql = "select createdTime from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1) order by createdTime limit 1"
	totalStartTimeTemp = businessTools.fetchData(totalStartTimeSql)
	totalStartTime = utils.timestampToTime(totalStartTimeTemp)
	dictTemp["totalStartTime"] = totalStartTime

	totalEndTimeSql = "select createdTime from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1) order by createdTime desc limit 1"
	totalEndTimeTemp = businessTools.fetchData(totalEndTimeSql)
	totalEndTime = utils.timestampToTime(totalEndTimeTemp)
	dictTemp["totalEndTime"] = totalEndTime

	totalExcuteTimeTemp = totalEndTimeTemp - totalStartTimeTemp
	totalExcuteTime = utils.secondToClock(totalExcuteTimeTemp)
	dictTemp["totalExcuteTime"] = totalExcuteTime


	if reportFileDemoPath is not None or reportFileDemoPath is not "":
		try:
			html_doc = utils.readFile(reportFileDemoPath)
			soup = BeautifulSoup(html_doc, "html.parser")
			for l in dictTemp:
				soup.find(id=l).string = str(dictTemp[l])

		except Exception, e:
			utils.logSave("修改html内容失败:" + str(e),"error")
	if reportFilePath is not None or reportFilePath is not "":
		try:
			if os.path.exists(reportFilePath):
				os.remove(reportFilePath)
			utils.writeToFile(reportFilePath, str(soup))
		except Exception, e:
			utils.logSave("修改html内容失败:" + str(e),"error")
	utils.logSave("渲染报告结束")

if __name__ == '__main__':
	html_doc = utils.readFile(config.reportFileDemoPath)
	soup = BeautifulSoup(html_doc, "html.parser")
	original_tag = soup.find(id="new_table")
	new_tag = soup.new_tag("tr", id="tr_1")
	original_tag.append(new_tag)
	original_tag1 = soup.find(id="tr_1")

	new_tag1 = soup.new_tag("td", id="number")
	original_tag1.append(new_tag1)	
	new_tag2 = soup.new_tag("td", id="number")
	original_tag1.append(new_tag2)		
	# <b><a href="http://www.example.com"></a></b>

	new_tag1.string = "1"
	new_tag2.string = "2"
	print soup
	# <b><a href="http://www.example.com">Link text.</a></b>
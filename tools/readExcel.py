#!/usr/bin/env python
# -*- coding:utf-8 -*-

# jp jsonSchema

import sys
import xlrd
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../setting")
import config
import datetime

class readExcel(object):
	"""docstring for ClassName"""
	def __init__(self, excelFile):
		super(readExcel, self).__init__()
		# print "[" + str(datetime.datetime.now()) + "]"+ "11"
		self.excelFile = excelFile
		# print "[" + str(datetime.datetime.now()) + "]"+ "22"
		self.data = xlrd.open_workbook(excelFile)
		# print "[" + str(datetime.datetime.now()) + "]"+ "33"
		# self.table = self.data.sheets()[tableSheet-1]


	def setTableSheet(self, tableSheet):
		self.tableSheet = tableSheet
		self.table = self.data.sheets()[tableSheet-1]


	def setTableSheet_by_name(self, tableSheetName):
		# print tableSheetName
		# print type(tableSheetName)
		# tableSheetName = unicode(tableSheetName,"utf-8")
		# self.table = self.data.sheet_by_name(tableSheetName)
		self.table = self.data.sheet_by_name(tableSheetName)

	def getSheetCount(self):
		return len(self.data.sheets())

	def getRows(self):
		nrows = self.table.nrows
		return nrows

	def getCols(self):
		ncols = self.table.ncols
		return ncols

	def read(self,rowNumber,colNumber):
		# nrows = self.table.nrows
		# ncols = self.table.ncols
		myData = self.table.row_values(rowNumber-1)
		result = myData[colNumber-1]
		return result

	def write(self,rowNumber,colNumber,value):
		print "Need xlwt module , not finished"


#当直接执行此文件时会执行以下内容
#以下内容包含一些使用方法
if __name__ == '__main__':
	filePath = config.apiTestCaseFilePath
	a = readExcel(filePath,1)	
	a.setTableSheet(1)
	a.setTableSheet_by_name("Sheet1")
	a.read(2,2)
	a.getSheetCount()


#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("business")
sys.path.append("tools")
import logging
import json
import re
import datetime
import time

def fetchData(sql):
    '''查询一条精确数据...'''
    print 44
    # fetchone_sql = 'SELECT name FROM student WHERE ID = ? '
    # data = 1
    filepath = r"C:\Users\zhoudonbin\Documents\GitHub\MyApiAuto\result\database\database.db"
    try:
    	print 55
        conn = sqliteHandler.get_conn(filepath)
        print 22
        print conn
        result = sqliteHandler.fetchoneExact(conn, sql)
        print result
    except Exception, e:
        result = ""        
    if result is None or result is "":
        return ""
    else:
        return result

def replaceString1(inputString):
    if isinstance(inputString,unicode):
        inputString = inputString.encode('utf-8')
    if isinstance(inputString,str):
        matchObj = re.search('\$\(\w*\)', inputString , re.M|re.I)
        if matchObj:
            stringTemp = matchObj.group()
            sql = "select passObjectValue from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1) and passObject='" + stringTemp[2:-1] + "' order by ID desc limit 1"
            sql = "select passObjectValue from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1) and passObject like '%" + stringTemp[2:-1] + "%' order by ID desc limit 1"
            print sql
            temp = fetchData(sql)
            print 33
            print temp
            if re.search('\[*\]',temp):
            	temp1 = json.loads(temp)
            else:
            	temp1 = ""
            #如果查询不到数据的话，暂时不做处理，以后扩展的时候加上用例依赖
            if temp1 is None or temp1 is "":
                resultString = inputString.replace(stringTemp,temp)
            else:
                resultString = inputString.replace(stringTemp,temp)
            return replaceString1(resultString)
        else:
            return inputString
    else:
        return inputString
inputString = "$(sid_id)"
matchObj = re.search('\$\(\w*\)', inputString , re.M|re.I)
stringTemp = matchObj.group()
# stringTemp = stringTemp[2:-1]
sql = "select passObjectValue from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1) and passObject like '%" + stringTemp[2:-1] + "%' order by ID desc limit 1"
print sql
# def stringToDict(mystring):
# 	if isinstance(mystring,unicode):
# 		mystring = mystring.encode("utf-8")
# 	if isinstance(mystring,str) and mystring is not "":
# 		if re.search('^{.*}$',mystring) or re.search('^[.*]$',mystring):
# 			try:
# 				return json.loads(mystring)
# 			except Exception, e:
# 				return mystring
# 	return mystring


# list1 = '["a","注册","1",1]'
# # mylist = json.loads(list1)
# # print mylist[3]
# if re.search('^{.*}$',list1) or re.search('^\[.*\]$',list1):
# 	print 11


# print stringToDict(list1)

# class myclass(object):
# 	"""docstring for myclass"""
# 	def __init__(self, string1):
# 		super(myclass, self).__init__()
# 		self.dict1 = self.stringToDict(string1)

# 	def stringToDict(self,mystring):
# 		if isinstance(mystring,str) and mystring is not "":
# 			if re.search('^{.*}$',mystring):
# 				try:
# 					print mystring
# 					return json.loads(mystring)
# 				except Exception, e:
# 					utils.logSave("stringToDict()出现异常，入参为：" + str(mystring) + e)
# 		return {}

# a1 = '{"$[code]":0,"$[data].[data[*].order_id":""}'
# # c = '{"登录":"正常登录","登录2":"异常登录操作5"}'
# a = myclass(a1)
# print a.dict1
# print a.dict1
# s = json.loads(c)
# print s
# print s.keys()




# a = '{"登录":"正常登录","登录":"异常登录操作5"}'
# b = {}
# c = {"a":1,"b":2}

# if b:
# 	print 11
# print len(c)
# print type(b)
# print type(json.loads(a))

# print int(10.0)
# print datetime.datetime.now()
# time.sleep(1.0)

# print datetime.datetime.now()

# testCaseModule = "登录"
# caseName = "正常登录"
# sql = "SELECT result FROM result where testCaseModule=" + "'" + testCaseModule + "'" + " and testCaseName="  + "'" + caseName + "'" + " and buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1)"
# print sql

# data1 = "app_version=1.4.0&app_client_id=4&"
# print data1[:-1]

# def myStrip(myString):
#     print type(myString)
#     if isinstance(myString, unicode):
#         myString = myString.encode('utf-8')

#     if isinstance(myString, str):
#         result = myString.replace(' ','').replace('\t','').replace('\r','').replace('\n','')
#     else:
#         result = myString
#     print type(result)
#     return result

# def test_myStrip():
#     string1 = '**  NN\tMM\rOO PP\nLL **'
#     string2 = u'**  NN\tMM\rOO PP\nLL **'
#     string3 = []
#     string4 = {"key":"value"}
#     string5 = 1
#     print myStrip(string1)
#     print myStrip(string2)
#     print myStrip(string3)
#     print myStrip(string4)
#     print myStrip(string5)
# test_myStrip()

# def dataProcess(inputString,myType,exceptionResult):
#     if isinstance(inputString,myType):
#         if myType == str:
#             inputString = myStrip(inputString)
#             return inputString
#         return inputString
#     else:
#         inputString = exceptionResult
#         return inputString

# a = "asdsa \t\nads"
# print dataProcess(a,str,"aa")

# print a
# print a.strip()
# print a.replace(' ','').replace('\t','').replace('\r','').replace('\n','')

# a = "app_version=1.3.0&id=13488"
# b = r'{"app_version":1}'
# print type(b)
# if re.search('^app_version\=',a) or re.search('\&app_version\=',a) or re.search('\"app_version\"\:',a):
# 	print 1

# if re.search('^|&' + 'app_version=',a):
# 	print 12
# unicodeString = u'{"order_status":0}'
# print unicodeString
# string = unicodeString.encode()
# print string

# data = {"a":1,"b":2}
# print type(data)
# data = json.dumps(data)
# print type(data)
# print data

# s=r'{"$.data.is_virtual":0,"$.data.status":1,"$.data.join_status":2,"$.data.is_show_button":1,"$.data.ticket":None,"$.data.shipping_fee":"0.00","$.data.button_status_text":"","$.data.tickets.sku_list[*].comment_rebate_price":"评价返￥12","$.data.comment_rebate_price":"25.00"}'
# print type(s)
# a=json.loads(s)
# print type(a)

#json.dumps(s.replace('\r\n', '\\r\\n'))

# aa = {"$.data.is_virtual":0,"$.data.status":1,"$.data.join_status":2,"$.data.is_show_button":1,"$.data.ticket":None,"$.data.shipping_fee":"0.00"}
# bb = {"$.data.is_virtual":0,"$.data.status":1,"$.data.join_status":2,"$.data.is_show_button":1,"$.data.ticket":None,"$.data.shipping_fee":"0.00"}
# aa={"$.data.button_status_text":"","$.data.tickets.sku_list[*].comment_rebate_price":"评价返￥12"}
# bb={"$.data.button_status_text":"","$.data.tickets.sku_list[*].comment_rebate_price":"评价返￥12"}
# print cmp(aa,bb)
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../business")
sys.path.append("../tools")
sys.path.append("../setting")
import businessTools
import re
import time
import json
import os
import logging
import config

list2 = [1,2,3]
list1 = [1,2,3,4,5]

for l in list1:
	if l not in list2:
		print 22


# logging.basicConfig(
# 				level=logging.DEBUG,
#                 format='[%(asctime)s] %(filename)s line:%(lineno)d [%(levelname)s]: %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename=config.logFilePath,
#                 filemode='a')

# # #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
# # console = logging.StreamHandler()
# # console.setLevel(logging.DEBUG)
# # formatter = logging.Formatter('%(asctime)s:[%(levelname)-8s] %(message)s')
# # console.setFormatter(formatter)
# # logging.getLogger('').addHandler(console)

# # logging.notset('This is notset message')
# logging.debug('This is debug message')
# logging.info('This is info message')
# logging.warning('This is warning message')
# logging.error('This is error message')
















# now = time.time()
# now2 = time.time()
# print int(now)
# path = os.path.dirname(sys.argv[0])
# print path
# os.chdir(os.path.dirname(sys.argv[0]))
# path = os.getcwd()
# print path


# temp = "hello"
# str3 = "http://haowan.mmbang.com/user/default/$(login)?mobile=&$(password)="
# if re.search('.*\$\([a-zA-Z]*\)',str3):
# 	print re.sub("\$\([a-zA-Z]*\)","hello",str3)

# str0 = "aaaabbcc"
# reg = "^a"
# str1 = '''{"user_id":"7229410","user_name":"冬瓜大神2","avatar":"http://img01.mmbang.info/1iyaya_group6_M02_AF_4A_CggaDVZyYaCASGMoAAAFOIe-vuk622.jpg"}'''
# str2 = '''lat=31.24916171&lng=121.48789949&screen_width=720&screen_height=1280&app_version=1.4&sid=811eb044ace3f96c75dab5a8b6b57605&sign=a2d47c7abc766075bd3996ef66e01d71'''
# str2 = ""
# if re.search('^{.*}$',str2):
# 	print "pass"
# elif re.search('.*=.*',str2):
# 	print "fail"
# else:
# 	print "aa"
# #print(re.search('www', 'www.runoob.com').span())

# # print str11
# print('#'*50 + "start" + '#'*50)

# expression_result = "pattern([^0])"
# pattern = '^pattern(.*)$'
# if re.search(pattern,expression_result):
# 	pattern1 = expression_result[8:-1]
# 	print pattern1
# else:
# 	print "fail"
# 	print pattern
# checkMode = "jsonpathno"
# if (checkMode.startswith("jsonpath")):
# 	print 111

# str = '''{"mobile":"","$(password)":""}'''
# str = '''{"$[msg]":"登录成功","$[code]":0}'''
# js = json.loads(str)

# line = "Cats are smarter than dogs"
# str1 = "http://haowan.mmbang.com/user/default/$(login)"
# str2 = '''{"$(mobile)":"","$(password)":""}'''
# matchObj = re.search('\$\(\w*\)', str2, re.M|re.I)

# if matchObj:
#    print "matchObj.group()===" + matchObj.group() + "=="
# else:
#    print "No match!!"



def replaceString(inputString):
	matchObj = re.search('\$\(\w*\)', inputString , re.M|re.I)
	if matchObj:
		stringTemp = matchObj.group()
		sql = "select passObjectValue from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1) and passObject='" + stringTemp[2:-1] + "' order by ID desc limit 1"
		temp = businessTools.fetchData(sql)
		return replaceString(inputString.replace(stringTemp,temp))
	else:
		return inputString

# print time.time()

# str1 = "http://haowan.mmbang.com/user/default/$(login)"
# str2 = '''{"$(mobile)":"","$(password)":""}'''
# print replaceString(str2)
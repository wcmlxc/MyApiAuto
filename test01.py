#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("business")
import logging
import json
import re

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
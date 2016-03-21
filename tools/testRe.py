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


import jsonpath

dict1 ={u'msg': u'', u'code': 0, u'data': 
{u'recommend_items': [{u'cover': u'http://mmb-shop.qiniu.mmbang.info/f1e62b341450852452761.jpg?imageView2/1/w/480/h/240', u'link': u'com.iyaya.haowan://app/shop/item/12361', u'id': u'12361', u'name': u'\u6211\u662f\u5c0f\u5c0f\u9676\u827a\u5e08\u2014\u2014\u827a\u7f18\u624b\u5de5\u574a'}, {u'cover': u'http://mmb-shop.qiniu.mmbang.info/e4f09e771451297509724.jpg?imageView2/1/w/480/h/240', u'link': u'com.iyaya.haowan://app/shop/item/12416', u'id': u'12416', u'name': u'\u666f\u9676\u9676\u827a\u4eb2\u5b50\u5957\u9910 \u53d8\u8eab\u5c0f\u5c0f\u9676\u827a\u5e08(\u666f\u9676\u793e\u533a\u5e97)'}, {u'cover': u'http://mmb-shop.qiniu.mmbang.info/103934d31451546227976.jpg?imageView2/1/w/480/h/240', u'link': u'com.iyaya.haowan://app/shop/item/12463', u'id': u'12463', u'name': u'\u7ea6\u65e6\u738b\u56fd\u795e\u5947\u7684\u74f6\u4e2d\u6c99\u753b \u74f6\u5b50\u91cc\u7684\u6c99\u753b\u827a\u672f'}, {u'cover': u'http://mmb-shop.qiniu.mmbang.info/34a67851453776273709.jpg?imageView2/1/w/480/h/240', u'link': u'com.iyaya.haowan://app/shop/item/12822', u'id': u'12822', u'name': u'\u5feb\u4e50\u57ce\u5821+\u9633\u5149\u6c99\u6ee9\u5168\u5929\u7545\u73a9\u5355\u4eba\u7968'}], 
u'service_support': [], u'age_range_desc': u'\u53ef\u552e\u5356\uff08\u5355\u89c4\u683c\u7535\u5b50\u7968\u4e0b\u5355', u'mom_comments': {u'comments_score': 5, u'items': [], u'title': u'\u5988\u5988\u79c0', u'more_params': {u'item_id': u'13512', u'page': 2}, u'comments_count': u'0', u'is_more': False}, u'is_need_identity': 0, u'ticket': {u'status': u'1', u'stock_num': 10, u'name': u'\u5957\u9910\u4e00', u'item_limit_buy': 0, u'st_id_1': u'0', u'st_id_3': u'0', u'st_id_2': u'0', u'st_id_4': u'0', u'comment_rebate_price': u'\u4e0b\u5355\u8fd4\uffe510', u'total_stock': 10, u'fridgecode': u'', u'comment_rebate_price_value': 0, u'limit_buy_num': 0, u'sale_price': 0.01, u'rebate_price': 10, u'origin_price': 10, u'id': u'16123', u'cost_price': u'8.00'}, u'apply_url': u'', u'button_status_text': u'', u'is_favorite': 0, u'buy_notice_view': u'http://haowan.mmbang.com/item/default/buyNoticeView?id=13512&csig=5bff89740ad04eddcc9120c18b4e1216', u'images': [u'http://mmb-shop.qiniu.mmbang.info/cca476df1458287811201.jpg?imageView2/1/w/480/h/240'], u'consult_count': 0, u'lng': 0, u'circum_facility': [1, 2, 3], u'sale_num_str': u'\u5df2\u552e0\u4ef6', u'thumb': u'http://mmb-shop.qiniu.mmbang.info/b050a541458287819476.jpg', u'id': u'13512', u'rebate_info': u'\u4e0b\u5355\u53ef\u8fd410.00\u5143', u'sub_title': u'\u53ef\u552e\u5356\uff08\u5355\u89c4\u683c\u7535\u5b50\u7968\u4e0b\u5355', u'is_virtual': 1, u'item_remark': u'\u53ef\u552e\u5356\uff08\u5355\u89c4\u683c\u7535\u5b50\u7968\u4e0b\u5355\u8fd4\uff09\u5546\u54c1', u'has_nav': True, u'is_show_button': 1, u'sale_price': u'0.01', u'consult_list': [], u'status': 1, u'tickets': None, u'is_app_recommend': 0, u'comment_rebate_price': 0, u'is_show_price': 1, u'share': {u'url': u'http://haowan.mmbang.com/wap/item/view?id=13512&s_from=appshare', u'title': u'\u597d\u73a9\u661f\u7403 - \u53ef\u552e\u5356\uff08\u5355\u89c4\u683c\u7535\u5b50\u7968\u4e0b\u5355\u8fd4\uff09\u5546\u54c1', u'thumb': u'http://mmb-shop.qiniu.mmbang.info/b050a541458287819476.jpg?imageView2/1/w/150/h/150', u'desc': u'\u53ef\u552e\u5356\uff08\u5355\u89c4\u683c\u7535\u5b50\u7968\u4e0b\u5355\u8fd4\uff09\u5546\u54c1'}, u'carriage_price': u'0.00', u'join_status': 2, u'address': u'\u78a7\u6ce2\u8def690\u53f72\u53f7\u697c302\u5ba4', u'lat': 0, u'merchant_info': {u'id': u'55', u'name': u'YS-\u5f00\u53d1\u6d4b\u8bd5\u5546\u6237'}, u'service_phone': u'4006162722', u'distance': u'', u'tour_note': {u'total_count': u'0', u'items': [], u'title': u'\u5988\u5988\u6e38\u8bb0'}, u'name': u'\u53ef\u552e\u5356\uff08\u5355\u89c4\u683c\u7535\u5b50\u7968\u4e0b\u5355\u8fd4\uff09\u5546\u54c1', u'comments_score': 5, u'origin_price': u'10.00', u'recommend_view': u'http://haowan.mmbang.com/item/default/recommend?id=13512&csig=5bff89740ad04eddcc9120c18b4e1216', u'comments_count': u'0', u'content_view': u'http://haowan.mmbang.com/item/default/content?id=13512&csig=5bff89740ad04eddcc9120c18b4e1216', u'app_recommend_txt': u'APP\n\u63a8\u8350', u'shipping_fee': u'0.00', u'sale_num': 0, u'rebate_price': u'10.00'}}
exe = {"$.data.join_status":0,"$.data.is_show_button":0}
v = jsonpath.jsonpath(dict1, "$.data.is_virtual")
v1 = jsonpath.jsonpath(dict1, "$.data.sku_list[*].comment_rebate_price")
print v
print v1










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
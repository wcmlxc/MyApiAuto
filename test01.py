#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("business")
import logging
import json
import re
a = "app_version=1.3.0&id=13488"
b = r'{"app_version":1}'
print type(b)
if re.search('^app_version\=',a) or re.search('\&app_version\=',a) or re.search('\"app_version\"\:',a):
	print 1
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
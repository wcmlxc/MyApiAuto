#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("business")
import logging
import json

unicodeString = u"报名未开始,敬请期待"
print type(unicodeString)
string = "报名未开始,敬请期待"
print type(string)
print unicodeString == string
# unicodeString = u'{"order_status":0}'
# print unicodeString
# string = unicodeString.encode()
# print string

# data = {"a":1,"b":2}
# print type(data)
# data = json.dumps(data)
# print type(data)
# print data
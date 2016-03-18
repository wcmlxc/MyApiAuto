#!/usr/bin/env python
# -*- coding:utf-8 -*-

# jp jsonSchema

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../business")
sys.path.append("../tools")
sys.path.append("../setting")
import businessTools
import emailSend
import utils
import config

def main():
	utils.logSave("开始发送报告")
	print "开始发送报告"
	mailto_list = config.mailto_list
	# html =  string + "<a href='http://10.192.74.15:80/AutoResult/Report/index.html'>接口测试报告</a>"
	html = utils.readFile(config.reportFilePath)
	emailSend.send_mail_html(mailto_list,"接口测试报告python自动发送(勿回)", html)
	utils.logSave("发送报告结束")
	print "发送报告结束"
if __name__ == '__main__':
	main()



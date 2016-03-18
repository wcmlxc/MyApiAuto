#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')


global FLAG_requests
FLAG_requests = 0
global FLAG_xlrd
FLAG_xlrd = 0
global FLAG_beautifulSoup4
FLAG_beautifulSoup4 = 0

listCmd = "pip list"
for l in os.popen(listCmd).readlines():
	# print l
	if "xlrd" in l:
		FLAG_xlrd = 1;
	if "requests" in l:
		FLAG_requests = 1;
	if "beautifulSoup4" in l:
		FLAG_beautifulSoup4 = 1;	

if FLAG_xlrd == 0:
	os.system("pip install xlrd")
if FLAG_requests == 0:
	os.system("pip install requests")
if FLAG_beautifulSoup4 == 0:
	os.system("pip install beautifulSoup4")
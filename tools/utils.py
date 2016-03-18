#!/usr/bin/env python
# -*- coding:utf-8 -*-

# jp jsonSchema

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../setting")
import config
import time
import logging
# import datetime
import os
# import simplejson

def createFile(filepath):
    dirfilepath = os.path.dirname(filepath)
    basefilepath = os.path.basename(filepath)
    
    if os.path.isdir(dirfilepath):
        pass
    else:
        logSave("创建Log文件夹成功")
        print "创建Log文件夹成功"
        os.makedirs(dirfilepath)  
         
    if os.path.isfile(filepath):
        logSave("创建log文件" + str(basefilepath) + "失败！ 文件已经存在")
        print "创建log文件" + str(basefilepath) + "失败！ 文件已经存在"
    else:
        logSave("创建log文件" + str(basefilepath) + "成功")
        print "创建log文件" + str(basefilepath) + "成功"
        f=open(filepath,'w')
        f.close()
     
# def createLogFile():
#     now=datetime.datetime.now()
#     nowtime = now.strftime('%Y') + "-" + now.strftime('%m') + "-" + now.strftime('%d') + "-" + now.strftime('%H') + "-" + now.strftime('%M') + "-" + now.strftime('%S')
#     logFile=APIconfig.APIconfig.LogDirPath + "\\" + nowtime +".log"
# #     print logFile
#     createFile(logFile)
#     return logFile

def writeToFile(filename,string):
    logSave("打开文件" + filename)
    print "打开文件" + filename
    f = open(filename,'a')
    try:
        logSave("开始写入文件" + filename)
        print "开始写入文件" + filename
        f.write(string+"\n")
        # print "写入" + string + "成功"
    except:
        logSave("写入" + string + "失败:" + str(e),"error")
        print "写入" + string + "失败"
    finally:
        logSave("关闭文件")
        print "关闭文件"
        f.close()

def readFile(filename):
    logSave("读取文件" + filename)
    print "读取文件" + filename
    try:
        f = open(filename).read()
        return f
    except Exception, e:
        logSave("读取文件内容失败:" + str(e),"error")
        print "读取文件内容失败:{}".format(e)
        return ""

    # try:
    #     print "开始读取文件" + filename
    #     f.write(string+"\n")
    #     print "写入" + string + "成功"
    # except:
    #     print "写入" + string + "失败"
    # finally:
    #     print "关闭文件"
    #     f.close()
def timestampToTime(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def secondToClock(sec):
    if isinstance(sec, int):
        hour = sec/3600
        minute = (sec%3600)/60
        minute = "%02d" % minute
        second = (sec%3600)%60
        second = "%02d" % second
        return str(hour) + ":" + str(minute) + ":" + str(second)
    else:
        logSave("请输入整数,否则返回NA:NA:NA","error")
        print "请输入整数,否则返回NA:NA:NA"
        return "NA:NA:NA"


def calPCT(a, b):
    if b == 0:
        pct = "0.00%"
        return pct
    else:
        a = float(a)
        b = float(b)
        pct = "%.2f%%" % ((a/b)*100)
        return pct

def logSave(msg, level="debug"):
    # if not os.path.exists(logFilePath):
    #     utils.createFile(logFilePath)
    if config.logFilePath is not None or config.logFilePath is not "":
        logging.basicConfig(
                        level=logging.DEBUG,
                        format='[%(asctime)s] %(filename)s line:%(lineno)d [%(levelname)s]: %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=config.logFilePath,
                        filemode='a')
        if level.lower() == "debug":
            logging.debug(msg)
        elif level.lower() == "info":
            logging.info(msg)
        elif level.lower() == "warning":
            logging.warning(msg)
        elif level.lower() == "error":
            logging.error(msg)
        else:
            logging.debug(msg)
    print msg
# def timeToTimestamp():
#     d=datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
#     return time.mktime(d.timetuple())
    
def listContains(list1,list2):
    for l in list1:
        if l not in list2:
            return False
    return True

def test_listContains():
    list1 = [1,2,3]
    list2 = [1,2,3,4,5]
    if listContains(list2,list1):
        print "Pass"
    else:
        print "Fail"

if __name__ == '__main__':
    pass
    filepath = config.logFilePath
    test_listContains()
    # createFile(filepath)
    # writeToFile(filepath,"hello")
    # print readFile(filepath)
    # print timeStampToTime(1381419600)
    # print secondToClock(10)
    # print calPCT(1,0)

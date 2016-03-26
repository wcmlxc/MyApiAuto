#!/usr/bin/env python
# -*- coding:utf-8 -*-

# jp jsonSchema

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../setting")
import config
sys.path.append("../tools")
from requestApi import requestApi
from testSQL import doSql
import sqliteHandler
import utils
from readExcel import readExcel
import time
import os
import json
import re
import logging

global logFilePath
logFilePath = config.logFilePath
global databaseFilePath
databaseFilePath = config.databaseFilePath
global SHOW_SQL
SHOW_SQL = True


def creatResultTable():
    '''创建结果收集表result...'''
    utils.logSave('''创建结果收集表result...''')
    sqlite = '''CREATE TABLE result
	    (ID                 INTEGER PRIMARY KEY AUTOINCREMENT,
	    testCaseNumber      INT,
        testCaseModule      CHAR(50),
	    testCaseName        CHAR(50),
	    apiName             CHAR(50),
	    apiNotice           CHAR(50),
        testCaseLevel       CHAR(50),
	    method              CHAR(50),
	    host                CHAR(50),
	    url                 CHAR(200),
	    data                CHAR(200),
        passObject          CHAR(50),
	    passObjectValue     CHAR(50),
	    checkMode           CHAR(50),
	    result              CHAR(50),
        errorMsg            CHAR(50),
	    responseTime        INT,
	    statusCode          INT,
	    buildTimes			INT,
	    createdTime         INT,
	    modifyTime          INT
	    );'''
    try:
        conn = sqliteHandler.get_conn(databaseFilePath)
        sqliteHandler.create_table(conn, sqlite)
        utils.logSave('创建结果收集表result正常')
    except Exception, e:
        utils.logSave('创建结果收集表result异常:' + str(e),"error")

def createBasicTable():
    '''创建公共请求参数表basic'''
    utils.logSave('''创建公共请求参数表basic''')
    sqlite = '''CREATE TABLE basic
        (app_client_id         INT,
        app_version         CHAR(50),
        sid                 CHAR(50),
        sign                CHAR(50)
        );'''
    try:
        conn = sqliteHandler.get_conn(databaseFilePath)
        sqliteHandler.create_table(conn, sqlite)
        sqlite2 = '''INSERT INTO basic (app_client_id, app_version) VALUES (4, "1.4.0")'''
        sqliteHandler.save(conn, sqlite2)
        utils.logSave('创建公共请求参数表basic正常')
    except Exception, e:
        utils.logSave("创建公共请求参数表basic异常:" + str(e),"error")


def insertTable(testCaseNumber, testCaseModule, testCaseName, apiName, apiNotice, testCaseLevel, method, host, url, data, passObject, passObjectValue, checkMode, result, errorMsg, responseTime, statusCode, buildTimes):
    now = int(time.time())
    '''数据库插入数据'''
    utils.logSave('''数据库插入数据...''')
    sqliteTemp1 = "INSERT INTO result (testCaseNumber,testCaseModule,testCaseName,apiName,apiNotice,testCaseLevel,method,host,url,data,passObject,passObjectValue,checkMode,result,errorMsg,responseTime,statusCode,buildTimes,createdTime,modifyTime) VALUES "
    sqliteTemp2 = "(" + str(testCaseNumber) + ",'" + str(testCaseModule) + "','" + testCaseName + "','" + apiName + "','" + apiNotice + "','" + testCaseLevel + "','" + method + "','" + host + "','" + url + "','" + data + "','" \
        + passObject + "','" + passObjectValue + "','" + str(checkMode) + "','" + str(result) + "','" + str(errorMsg) + "'," + str(responseTime) + "," + str(
            statusCode) + "," + str(buildTimes) + ",'" + str(now) + "','" + str(now) + "')"
    sqlite = sqliteTemp1 + sqliteTemp2
    try:
        conn = sqliteHandler.get_conn(databaseFilePath)
        sqliteHandler.save(conn, sqlite)
        utils.logSave('数据库插入数据正常')
    except Exception, e:
        utils.logSave("数据库插入数据异常:" + str(e),"error")
    # ds = doSql()
    # ds.excuteSql(sqlite)

def updateSid(sid):
    try:
        utils.logSave('更新数据sid字段开始')
        sqlite = "UPDATE basic SET sid = '" + sid + "'"
        conn = sqliteHandler.get_conn(databaseFilePath)
        sqliteHandler.updateAll(conn, sqlite)
        utils.logSave('数据库sid字段更新成功')
    except Exception, e:
        utils.logSave("数据库sid字段更新异常:" + str(e),"error")

def updateSign(sign):
    try:
        utils.logSave('更新数据sign字段开始')
        sqlite = "UPDATE basic SET sign = '" + sign + "'"
        conn = sqliteHandler.get_conn(databaseFilePath)
        sqliteHandler.updateAll(conn, sqlite)
        utils.logSave('更新数据sign字段成功')
    except Exception, e:
        utils.logSave("更新数据sign字段异常:" + str(e),"error")

def fetchData(sql):
    '''查询一条精确数据...'''
    utils.logSave('查询一条精确数据...')
    # fetchone_sql = 'SELECT name FROM student WHERE ID = ? '
    # data = 1
    try:
        conn = sqliteHandler.get_conn(databaseFilePath)
        result = sqliteHandler.fetchoneExact(conn, sql)
    except Exception, e:
        utils.logSave(str(e),"error")
        result = ""        
    if result is None or result is "":
        return ""
    else:
        return result

def replaceString(inputString):
    matchObj = re.search('\$\(\w*\)', inputString , re.M|re.I)
    if matchObj:
        stringTemp = matchObj.group()
        sql = "select passObjectValue from result where buildTimes=(select distinct buildTimes from result order by buildTimes desc limit 1) and passObject='" + stringTemp[2:-1] + "' order by ID desc limit 1"
        temp = fetchData(sql)
        #如果查询不到数据的话，暂时不做处理，以后扩展的时候加上用例依赖
        if temp is None or temp is "":
            resultString = inputString.replace(stringTemp,temp)
        else:
            resultString = inputString.replace(stringTemp,temp)
        return replaceString(resultString)
    else:
        return inputString


def dataPlus(data, myDict, skipList=[]):
    '''实现字符串拼接'''
    utils.logSave("打印dataPlus入参data:" + str(data))
    print "打印dataPlus入参data:{}和入参类型:{}".format(data,type(data))
    if data is None or data is "" or myDict is None or myDict is "":
        utils.logSave("dataPlus传入参数data或myDict为空","error")
        return ""
    if not isinstance(myDict, dict):
        utils.logSave("dataPlus传入参数myDict不是字典","error")
        return ""
    if not isinstance(skipList, list):
        utils.logSave("dataPlus传入参数skipList不是list","error")
        return ""
    print "打印dataPlus入参data:{}和入参类型:{}".format(data,type(data))
    try:
        if isinstance(data, unicode):
            data = data.encode()
        if isinstance(data, dict):
            data = json.dumps(data)
        if isinstance(data, str):
            if re.search('^{.*}$',data):
                for l in myDict:
                    if l in skipList:
                        continue
                    sql = 'SELECT ' + l +' FROM basic'
                    strTemp = ',"' + str(l) + '":"' + str(fetchData(sql)) + '"}'
                    data = data[:-1] + strTemp
                utils.logSave("打印出参data:" + str(data))
                print "打印出参data:{}".format(data)
                return data            
            else:
                for l in myDict:
                    if l in skipList:
                        continue
                    sql = 'SELECT ' + l +' FROM basic'
                    strTemp = "&" + str(l) + "=" + str(fetchData(sql))
                    data = data + strTemp
                utils.logSave("打印出参data:" + str(data))
                print "打印出参data:{}".format(data)
                return data
        else:
            utils.logSave("dataPlus参数错误data:" + str(data))
            return ""
    except Exception, e:
        utils.logSave("dataPlus处理出现异常:" + str(e),"error")
        return ""

def typeHandle(myobject, mytype):
    '''only support int,float,str,bool,dict; list is not supported yet'''
    if mytype == int:
        return int(myobject)
    elif mytype == float:
        return float(myobject)
    elif mytype == str:
        return str(myobject)
    elif mytype == list:
        # myobject = str(myobject)[1:-1]
        # l = myobject.split(",")
        # rl = []
        # for x in xrange(0,len(l)):
        # 	if l[x].startswith('"') and l[x].endswith('"'):
        # 		l[x] = l[x][1:-1]
        # 	elif l[x]
        # 	rl.append(l[x])
        # for y in xrange(0,len(rl)):
        # 	print rl[y]
        # return rl
        pass
    elif mytype == dict:
        myobject = json.loads(myobject)
        return myobject
    elif mytype == bool:
        return bool(myobject)

    # def createLogFile():
#     now=datetime.datetime.now()
#     nowtime = now.strftime('%Y') + "-" + now.strftime('%m') + "-" + now.strftime('%d') + \
        # "-" + now.strftime('%H') + "-" + now.strftime('%M') + "-" + now.strftime('%S')
#     logFile=APIconfig.APIconfig.LogDirPath + "\\" + nowtime +".log"
# print logFile
#     createFile(logFile)
#     return logFile

def returnValue(json, passObject):
    '''在一个json中循环查找passObject的值'''
    for d in json:
        if d == passObject:
            return json[d]
        elif isinstance(json[d],dict):
            return returnValue(json[d],passObject)
    return ""

def getSign(data):
    if data is None or data is "":
        data = ""
    if isinstance(data,str):
        if re.search('^{.*}$',data):
            data = json.loads(data)
    print data
    fullurl = config.getSingUrl
    #fullurl = "http://master.shop.mmbang.net/user/test/sign"
    req = requestApi(fullurl,data)
    req.get()
    utils.logSave("发送的URL:" + str(req.getUrl()))
    print "1111发送的URL:{}".format(req.getUrl())
    utils.logSave("获取到的返回报文:" + str(req.getJson()))
    print "获取到的返回报文:{}".format(req.getJson())
    result = returnValue(req.getJson(),"sign")
    updateSign(result)
    #return result

def dataProcess(inputData,myType,exceptionResult):
    if isinstance(inputData,unicode):
        inputData = inputData.encode('utf-8')
    if isinstance(inputData,myType) and inputData is not "":
        if myType == str:
            inputData = myStrip(inputData)
            return inputData
        return inputData
    else:
        inputData = exceptionResult
        return inputData

def myStrip(myString):
    # print type(myString)
    if isinstance(myString, unicode):
        myString = myString.encode('utf-8')

    if isinstance(myString, str):
        result = myString.replace(' ','').replace('\t','').replace('\r','').replace('\n','')
    else:
        result = myString
    # print type(result)
    return result

def test_myStrip():
    string1 = '**  NN\tMM\rOO PP\nLL **'
    string2 = u'**  NN\tMM\rOO PP\nLL **'
    string3 = []
    string4 = {"key":"value"}
    print myStrip(string1)
    print myStrip(string2)
    print myStrip(string3)
    print myStrip(string4)

def test_returnValue():
    json = {u'msg': u'\u767b\u5f55\u6210\u529f', u'code': 0, u'data': {u'pkey': u'3dfbee7c57232f47', u'user_id': u'48746', u'score': 71.89, u'password_exists': True, u'mobile': u'13661962542', u'gender': u'3', u'region': None, u'nick_name': u'\u5468\u51ac\u5f6c\u5988\u5988\u5e2e', u'birthday': None, u'avatar': u'http://ddxq-shop.u.qiniudn.com/FlIUzatUbCt3_B5UomLjls0r2LQL?imageView2/1/w/150/h/150', u'sid': u'b17e45704a84deb611730c6aaf389b3c'}}
    passO = "sid"
    print returnValue(json,passO)

def test_typeHandle():
    apiTestCaseFilePath = r"C:\Users\zhoudonbin\Desktop\APIAuto\test\testForTypeHandle.xlsx"
    excel = readExcel(apiTestCaseFilePath)
    excel.setTableSheet(1)
    print typeHandle(excel.read(1,1),int)
    # print typeHandle(excel.read(1,1),float)
    # print typeHandle(excel.read(1,2),str)
    # print typeHandle(excel.read(1,3),str)
    # print typeHandle(excel.read(1,4),str)
    # print typeHandle(excel.read(1,5),str)
    # print typeHandle(excel.read(1,6),bool)
    # print typeHandle(excel.read(1,7),bool)
    print typeHandle(excel.read(1, 9), dict)

def test_getSign():
    print('#'*50)
    print "test_getSign() Start......"
    data1 = "lat=31.24916171&lng=121.48789949&screen_width=640&screen_height=1136&app_version=1.4&sid=e4102eb998121d18ffccbfe2ce01d275"
    data1 = "item_id=12787&ticket_info=%5B%7B%22tid%22%3A%2212978%22%2C%22num%22%3A1%7D%5D&consignee=12&mobile=13661962542&sid=e4102eb998121d18ffccbfe2ce01d275"
    data2 = {"lat":31.24916171,"lng":121.48789949,"screen_width":640,"screen_height":1136,"app_version":1.4,"sid":"e4102eb998121d18ffccbfe2ce01d275"}
    data2 = {"item_id":12787,"ticket_info":[{"tid":"12978","num":1}],"consignee":"12","mobile":13661962542,"app_client_id":"1","app_version":"1.4.0","sid":"853eced8f096589ba102f603b41b7726","sign":"7e3aee1c524f291db682f64002fb9dc1"}
    print "第一种方式（字符串方式）获取sign：{}".format(getSign(data1))
    print "第二种方式（json方式）获取sign：{}".format(getSign(data2))
    print "test_getSign() End......"
    print('#'*50)

if __name__ == '__main__':

    #test_typeHandle()
    #test_returnValue()
    test_getSign()
    # utils.logSave("xxxx")
    # utils.logSave("xxxx11")
    # creatTable()
    # insertTable(1,"好玩星球","P1","XXX","XX","get","host","url","data","passObject","checkMode","result",1900,200,1)
    # a = fetchData('SELECT method FROM result WHERE ID = 7')
    # print a

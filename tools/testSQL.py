#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../setting")
import config
import utils

filePath = os.path.dirname(config.databaseFilePath)
database = os.path.basename(config.databaseFilePath)

class doSql:
    """一个实例执行一条sql语句 """
    def __init__(self,database=database,filePath=filePath):
        self.database = database
        self.filePath = filePath
        os.chdir(filePath)
        print "start sql connection"
        self.conn = sqlite3.connect(self.database)
    
    def excuteSql(self,sql):
        try:
            self.conn.execute(sql)
            self.conn.commit()
            print "excute sql pass"
        except Exception, e:
            print "excute sql fail"
        finally :
            print "close sql connection"
            self.conn.close()

    def fetchSql(self,sql):
        try:
            self.cu = self.conn.cursor()
            self.cu.execute(sql)
            print "fetchSql pass"
            return self.cu.fetchall()[0][0]
        except Exception, e:
            print e
            print "fetchSql fail"
        finally:
            pass

if __name__ == '__main__':
    sqlite = '''CREATE TABLE result
        (ID                 INTEGER PRIMARY KEY AUTOINCREMENT,
        testCaseNumber      INT,
        testCaseName        CHAR(50),
        testCaseLevel       CHAR(50),
        apiDescription      CHAR(50),
        apiNotice           CHAR(50),
        method              CHAR(50),
        host                CHAR(50),
        url                 CHAR(200),
        data                CHAR(200),
        passObject          CHAR(50),
        checkPoint          CHAR(50),
        result              CHAR(50),
        responseTime        INT,
        statusCode          INT,
        buildTimes          INT,
        createdTime         DATE,
        modifyTime          DATE
        );'''

    res = {u'msg': u'\u7528\u6237\u4fe1\u606f\u66f4\u65b0\u6210\u529f', u'code': 1, u'data': {u'user_status': 2}}

    selectSqlFromDB = '''
    select ID from result where ID=1
    '''
    
    # ds = doSql()
    # ds.excuteSql(sqlite)
    # print "111"

    ds2 =doSql()
    print ds2.fetchSql(selectSqlFromDB)
    print "222"
    
      
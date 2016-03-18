#!/usr/bin/env python
# -*- coding:utf-8 -*-

# jp jsonSchema

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../setting")
import time
import utils
import requests
import jsonpath

# 遇到网络问题（如：DNS查询失败、拒绝连接等）时，Requests会抛出一个ConnectionError 异常。
# 遇到罕见的无效HTTP响应时，Requests则会抛出一个 HTTPError 异常。
# 若请求超时，则抛出一个 Timeout 异常。
# 若请求超过了设定的最大重定向次数，则会抛出一个 TooManyRedirects 异常。
# 所有Requests显式抛出的异常都继承自 requests.exceptions.RequestException 。
class requestApi(object):
    """For More See ====> http://www.python-requests.org/en/master/user/quickstart/
        一些异常尚未封装
    """
    def __init__(self,fullurl,data={},timeout=60):
        super(requestApi, self).__init__()
        self.fullurl = fullurl
        self.data = data
        self.timeout = timeout

    def get(self):
        try:
            self.requestStartTime = time.time()
            self.request = requests.get(self.fullurl, params=self.data,timeout=self.timeout)
            self.requestEndTime = time.time()
            self.responseTime = round((self.requestEndTime - self.requestStartTime)*1000)
            utils.logSave("request pass")
            print "request pass"
        except Exception, e:
            utils.logSave("request error" + str(e),"error")
            print "request error"

    def post(self):
        try:
            self.requestStartTime = time.time()
            self.request = requests.post(self.fullurl, params=self.data,timeout=self.timeout)
            self.requestEndTime = time.time()
            self.responseTime = round((self.requestEndTime - self.requestStartTime)*1000)
            utils.logSave("request pass")
            print "request pass"
        except Exception, e:
            utils.logSave("request error" + str(e),"error")
            print "request error"

    def setData(self,data):
        self.data = data

    def setFullUrl(self,fullurl):
        self.fullurl = fullurl

    def getResponseTime(self):
        return self.responseTime

    def getUrl(self):
        self.url = self.request.url
        return self.url

    def getStatusCode(self):
        self.statusCode = self.request.status_code
        return self.statusCode

    def getHeaders(self):
        self.headers = self.request.headers
        return self.headers

    def getText(self):
        self.text = self.request.text
        return self.text

    def getEncoding(self):
        self.encoding = self.request.encoding
        return self.encoding

    def setEncoding(self,myEncoding):
        self.request.encoding = myEncoding
    
    def getJson(self):
        try:
            self.json = self.request.json()
            return self.json
        except Exception, e:
            utils.logSave("getJson error" + str(e),"error")
            print "getJson error"
            return {}
        
        
    # def get(fullurl,data):
    #     start_time = time.time()
    #     r = requests.get(fullurl, params=data)
    #     end_time = time.time()
    #     deltime = round((end_time - start_time)*1000)
    #     # utils.writeToFile(APIconfig.getLogFilePath(), "耗时：" + str(deltime) + "ms")
    #     # utils.writeToFile(APIconfig.getLogFilePath(), "返回码：" + str(r.status_code))
    #     # utils.writeToFile(APIconfig.getLogFilePath(), "返回报文：" + str(r.text))
    #     print r.url
    #     print r.response
    #     resjson =r.json()
    #     return resjson
        
    # def post(fullurl,data):
    #     start_time = time.time()
    #     r = requests.post(fullurl, params=data)
    #     end_time = time.time()
    #     deltime = round((end_time - start_time)*1000)
    #     # utils.writeToFile(APIconfig.getLogFilePath(), "耗时：" + str(deltime) + "ms")
    #     # utils.writeToFile(APIconfig.getLogFilePath(), "返回码：" + str(r.status_code))
    #     # utils.writeToFile(APIconfig.getLogFilePath(), "返回报文：" + str(r.text))    
    #     resjson =r.json()
    #     return resjson

# def HTTP_request(host,url,method,data):
#     '''
#     request work through httplib
#     futher can adjust it to unirest 
#     http://unirest.io/python.html
#     '''
#     try:        

# #         print start_time
#         if  method.upper()=="GET":
#             dataTemp = urllib.urlencode(data)   
#             conn1 = httplib.HTTPConnection(host,timeout=10)
#             #记录请求开始时间
#             start_time = time.time()
#             conn1.request("GET", url+'?'+dataTemp)
#         elif method.upper()=="POST":
#             conn1 = httplib.HTTPConnection(host,timeout=10)
#             #记录请求开始时间
#             start_time = time.time()            
#             conn1.request("POST", url, data)
            
#         res1 = conn1.getresponse()
        
#         #记录请求结束时间
#         end_time = time.time()
# #         print end_time
        
#         #计算请求时间（结果以ms计算）
#         #request response time(ms) 
#         deltime = round((end_time - start_time)*1000)
# #         print "接口用时：" + str(deltime) + " ms"
# #         print deltime

#         responseData = res1.read()
# #         responseData = responseData.decode('unicode_escape')
#         responseCode = res1.status
# #         ExceptedData = ExceptedData.encode('utf-8')
#         utils.writeToFile(APIconfig.getLogFilePath(), "耗时：" + str(deltime) + "ms")
#         utils.writeToFile(APIconfig.getLogFilePath(), "返回码：" + str(responseCode))
#         utils.writeToFile(APIconfig.getLogFilePath(), "返回报文：" + responseData)

        
#     except socket.error:
#         print(u"请求超时")
#         print(socket.error)
#         return False
        
#     finally:
#         if conn1:
#             conn1.close()

#     print json.loads(responseData)["msg"].encode('utf-8')
#     print type(json.loads(responseData))
#     print json.dumps(responseData,ensure_ascii=False)
#     return  json.loads(responseData)

if __name__ == '__main__': 
    # LogFilePath = utils.createLogFile(sys.argv[0])
    # APIconfig.setLogFilePath(LogFilePath)
    fullurl = "http://mbox.mmbang.net/Index/LoadIndex"
    #data = {"user_id":"7229410","user_name":"冬瓜大神2","avatar":"http://img01.mmbang.info/1iyaya_group6_M02_AF_4A_CggaDVZyYaCASGMoAAAFOIe-vuk622.jpg"}
    #print type(data)
    assertdata="用户信息更新成功"
    #a = requestApi("http://haowan.mmbang.com/home/default/index", {"user_id":"7229410","user_name":"冬瓜大神2","avatar":"http://img01.mmbang.info/1iyaya_group6_M02_AF_4A_CggaDVZyYaCASGMoAAAFOIe-vuk622.jpg"})
    fullurl = "http://haowan.mmbang.com/order/default/submit"
    data = {"item_id":12787,"ticket_info":'[{"tid":"12978","num":1}]',"consignee":12,"mobile":13661962542,"vcode":"","app_client_id":4,"app_version":1.4,"sid":"8f96e06a720d6ad17781921363a4da0f","sign":"7da5ebdc17b98f7c1909b1b77f065573"}
    data = '''item_id=12787&ticket_info=[{"tid":"12978","num":1}]&consignee=12&mobile=13661962542&vcode=&app_client_id=4&app_version=1.4&sid=8f96e06a720d6ad17781921363a4da0f&sign=7da5ebdc17b98f7c1909b1b77f065573'''
    #http://haowan.mmbang.com/order/default/submit?item_id=12787&ticket_info=%5B%7B%22tid%22%3A%2212978%22%2C%22num%22%3A1%7D%5D&consignee=12&mobile=13661962542&vcode=&app_client_id=4&app_version=1.4&sid=8f96e06a720d6ad17781921363a4da0f&sign=7da5ebdc17b98f7c1909b1b77f065573  
    a = requestApi(fullurl,data)
    a.post()
    a.getResponseTime()
    a.getUrl()
    a.getStatusCode()
    # a.getHeaders()['content-type']
    print a.getText()
    # a.getEncoding()
    # a.setEncoding('utf-8')
    # a.getEncoding()
    print a.getJson()
    result = jsonpath.jsonpath(a.getJson(), "$.[msg]")[0].encode()
    print len(result)
    print result
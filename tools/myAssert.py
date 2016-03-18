#!/usr/bin/env python
# -*- coding:utf-8 -*-

# from jsonpath_rw import jsonpath,parse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../setting")

def assertDictContains(fatherDict, sondict):

    if type(fatherDict) == dict and type(sondict) == dict:
        for k in sondict:
            print k
            if type(sondict[k]) == str or type(sondict[k]) == int or type(sondict[k]) == unicode or type(sondict[k]) == bool:
                print "进入单层的字典逻辑"
                for k2 in fatherDict:
                    if k == k2:
                        if fatherDict[k] == sondict[k]:
                            print 3
                            return "Pass"
            if type(sondict[k]) == dict:
                print 4
                return  assertDictContains(fatherDict,sondict[k])
            if type(sondict[k]) == list:
                print 5
                return  assertDictContains(fatherDict,sondict[k])
        print 6
        return "Fail"
    else:
        print type(fatherDict)
        print type(sondict)
        return "Exception"


def function():
    pass
# def function():
#     str ='''["code"]==0&&["data"]["calendar"]["27"]==1'''
#     t = str.split("&&")
#     print t
#     # print len(t)
#     for x in xrange(0,len(t)):
#         print t[x]
#         key = t[x].split("==")[0]
#         val = t[x].split("==")[1]


def test_cmp():
    '''测试字典完全相等 '''
    dict1 = {"code": 0,"msg": "","data": {"calendar": {"201602": {"27": 1,"28": 4},"201603":{"04":2,"05":22,"12":19,"20":12,"06":22,
        "19":13,"13":12,"26":9,"27":10},"201604":{"10":1,"16":1,"24":3,"02":1,"03":1,"22":1,"23":1,"29":1,"30":2}},"today":"20160229"}}
    dict2 = {"code":0,"msg":"","data":{"calendar":{"201602":{"27":1,"28":4},"201603":{"04":2,"05":22,"12":19,"20":12,"06":22,
        "19":13,"13":12,"26":9,"27":10},"201604":{"10":1,"16":1,"24":3,"02":1,"03":1,"22":1,"23":1,"29":1,"30":2}},"today":"20160229"}}
    print "测试字典完全相等cmp(dict1,dict2):"
    print cmp(dict1, dict2)
    print('#'*50)


def test_assertDictContains():
    '''测试字典包含'''
    dict1 = {"code":0,"msg":["first","second"],"data":{"calendar":{"201602":{"27":1,"28":4},"201603":{"04":2,"05":22,"12":19,"20":12,
        "06":22,"19":13,"13":12,"26":9,"27":10},"201604":{"10":1,"16":1,"24":3,"02":1,"03":1,"22":1,"23":1,"29":1,"30":2}},"today":"20160229"}}
    dict2 = {"code":0}
    dict3 = {"04":2}
    dict4 = {"201602":{"27":1,"28":4}}
    dict5 = {"msg":["first","second"]}
    print type(dict5)
    print "测试字典包含assertDictContains(fatherDict,sondict):"
    # print Root()
    print assertDictContains(dict1, dict2)
    print assertDictContains(dict1, dict3)
    print assertDictContains(dict1, dict4)
    print assertDictContains(dict1, dict5)
    print('#'*50)

if __name__ == '__main__':
    test_cmp()
    test_assertDictContains()
    # dictTwo = {"04":2}
    # dictTwo =     {"code":0,"msg":"","data":{"calendar":{"201602":{"27":1,"28":4},"201603":{"04":2,"05":22,"12":19,"20":12,"06":22,"19":13,"13":12,"26":9,"27":10},"201604":{"10":1,"16":1,"24":3,"02":1,"03":1,"22":1,"23":1,"29":1,"30":2}},"today":"20160229"}}
    # dictTwo = {'201602': {'27': 1, '28': 4}}
    # print cmp(dictOne,dictTwo)

    # dictOne = str(dictOne)
    # dictTwo = str(dictTwo)
    # if dictTwo.split("{")[1].split("}")[0] in fatherDict:
    #     print "pass"
    # else:
    #     print fatherDict
    #     print dictTwo
    #     print "fail"
    # a = assertDictContains(fatherDict,dictTwo)
    # print a

    #print assertDict(fatherDict,myDict)

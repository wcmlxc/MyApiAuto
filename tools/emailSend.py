#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import smtplib  
from email.mime.text import MIMEText
import utils

mailto_list=["azdbaaaaaa@163.com"] 
mail_host="smtp.163.com"  #设置服务器
mail_user="azdbaaaaaa"    #用户名
mail_pass="19880213"   #口令 
mail_postfix="163.com"  #发件箱的后缀
  
def send_mail_html(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
    me="周冬彬"+"<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        s = smtplib.SMTP()  
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()  
        return True  
    except Exception, e:
        utils.logSave(str(e),"error")
        print str(e)  
        return False  

def send_mail_txt(to_list,sub,content):  
    me="周冬彬"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:
        utils.logSave(str(e),"error")  
        print str(e)  
        return False  

if __name__ == '__main__':  
    # print "Start"
    # if send_mail_txt(mailto_list,"hello","hello world！"):  
    #     print "发送txt成功"  
    # else:  
    #     print "发送txt失败"

    if send_mail_html(mailto_list,"hello","<a href='http://10.192.74.15:80/AutoResult/Report/index.html'>接口测试报告</a>"):  
        print "发送html成功"  
    else:  
        print "发送html失败"
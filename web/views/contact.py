import json
from django.http import JsonResponse
from django.shortcuts import render    
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class SendEmail(object):
    def __init__(self,user_name,user_email,message):
        self._user_name=user_name
        self._user_email=user_email
        self._message=message
        self.host="smtp.mxhichina.com"  #设置服务器
        self.send_user=""    #用户名
        self.send_pass=""   #口令 
        self.reciver="" #接收邮件

    def send_email(self):
        mail_msg='''
        <p>用户名:{}</p>
        <p>邮箱地址:{}</p>
        <p>留言内容:{}</p>
        '''.format(self._user_name,self._user_email,self._message)
        message = MIMEText(mail_msg, 'html', 'utf-8') 
        message['From'] = Header('greasezone.cn', 'utf-8')
        message['To'] =  Header(self.reciver, 'utf-8')
        
        subject = '来自《古赵中都》网站的用户留言！'
        message['Subject'] = Header(subject, 'utf-8')  
        
        try:
            smtpObj = smtplib.SMTP_SSL(self.host,465) 
            smtpObj.login(self.send_user,self.send_pass) 
            smtpObj.sendmail(self.send_user,self.reciver, message.as_string())
            print('邮件发送成功！')
            return 0
        except Exception as e:
            print ("Error: 无法发送邮件",e) 
            return -1
        
    


def email(request):   
    if request.method=='GET':
        return render(request, 'index.html')
    else: 
        data=request.POST
        if 'name' not in data:
            result={'code':-1,'msg':'请录入用户名称！'}
        elif 'email' not in data:
            result={'code':-1,'msg':'请录入邮箱地址！'}
        elif 'message' not in data:
            result={'code':-1,'msg':'请录入发送的内容！'}
        else:
            result={'code':0,'msg':'发送成功！'}
        user_name=data['name']
        user_email=data['email']
        message=data['message'] 
        send_result=SendEmail(user_name,user_email,message).send_email()
        if send_result==0:
            result={'code':0,'msg':'发送成功！'}
        else:
            result={'code':-1,'msg':'系统繁忙！请用以下其它联系方式！'}
        return JsonResponse(result)  

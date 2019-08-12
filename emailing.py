# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 19:21:26 2019

@author: Chris
"""

import smtplib

port = 587  # For SSL
pwd = input("Type email password to get an email: ")
emailFrom = "chrisr4444@hotmail.com"
def sendEmail(subject="", content="",to="chrisr4@hotmail.co.uk"):
    if pwd=="":
        print('no password -> no email')
        return
    server = smtplib.SMTP('smtp.live.com', 587)
    server.starttls()
    server.login(emailFrom, pwd)
    toCheck = False
    if len(subject) + len(content) == 0:
        toCheck=True
    while toCheck:
        subject = input("Subject : ")
        content = input("Message : ")
        check =  input("Ok to send?.... \nEnter = Send\nSpace = Try again\n'abort' = Cancel\n")
        if check == '':
            toCheck = False
        if check == 'abort':
            print('Aborted - message not sent')
            return
    message = (f"From : {emailFrom}\r\n"+ f"To : {to}\r\n"+ f"Subject : {subject}\r\n"+ "\r\n"+ content)
    server.sendmail("chrisr4444@hotmail.com",to, message)
    print('Message sent')
    
    #to = "chrisr4@hotmail.co.uk"#input("\nTo : ")
    #subject = "fresh new subject line"#input("Subject : ")
    #content = "nice"#input("Message : ")


#import smtplib
#import string
#
#def send_email(to, subject, content):
#
#    emailFrom = emailFrom
#    pwd = password
#    to = "chrisr4@hotmail.co.uk"#input("\nTo : ")
##    subject = "new one"#input("Subject : ")
##    content = "trying again"#input("Message : ")
#    message = (f"From : {emailFrom}\r\n"+
#        f"To : {to}\r\n"+
#        f"Subject : {subject}\r\n"+
#        ""+
#        content)
#    server = smtplib.SMTP('smptp.live.com', 587)
##    server.ehlo()
#    server.starttls()
##    server.ehlo()
#    server.login(emailFrom, pwd)
#    server.sendmail(emailFrom, to, message)
##    server.close()
#    
#if __name__ == "__main__":
#    main()
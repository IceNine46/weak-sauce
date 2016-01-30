'''
Created on Dec 24, 2015

@author: Greg
'''
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

class Mail(object):
    '''
    classdocs
    Basic smtp helper class.
    For gmail accounts this method requires the less secure sign-in techonolgy to be enabled.
    https://www.google.com/settings/security/lesssecureapps
    '''

    '''
    Initialize the helper class with smtp server connection information.
    '''
    def __init__(self, server, port=587):
        self.server = server
        self.port = port
        self.session = None
        self.user = None
    
    '''
    Connect to the server using the USER's credentials.
    '''
    def connect(self, user, password):
        self.session = smtplib.SMTP(self.server, self.port)
        self.session.ehlo()
        self.session.starttls()
        self.session.login(user, password)
        self.user = user
    
    '''
    Send a message.
    '''  
    def send(self, recipient, subject, body, attachment=None, filename=None):
  
        msg = MIMEMultipart(
            From=self.user,
            To=COMMASPACE.join(recipient),
        )
        
        msg.add_header("Subject", subject)
        msg.add_header("Date", formatdate(localtime=True))
        msg.attach(MIMEText(body))
        
        if attachment != None:
            
            if filename == None:
                filename = "document.txt"
            
        msg.attach(MIMEApplication(
            attachment,
            Content_Disposition='attachment; filename="%s" % filename',
            Name="document.txt"
        ))
            
        '''
        headers = "\r\n".join(["from: " + self.user,
                   "subject: " + subject,
                   "to: " + recipient,
                   "mime-version: 1.0",
                   "content-type: text/html"])
        
        # body_of_email can be plaintext or html!                    
        content = headers + "\r\n\r\n" + body
        '''
               
        self.session.sendmail(self.user, recipient, msg.as_string())
        self.session.close()
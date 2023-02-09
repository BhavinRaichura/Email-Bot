import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import time


class Mailbot:
    def __init__(self, admin_email, admin_pass):
        self.obj = imaplib.IMAP4_SSL('imap.gmail.com',993)
        self.obj.login(admin_email, admin_pass)

    def bounce_res_by_postman(self, email_in_question):
        time.sleep(2)
        self.obj.select()
        result, data = self.obj.search(None, f'(FROM "Postmaster" SUBJECT "Undeliverable: An Appeal to add in fragrances of our Alumni Bondage")' )
        if(len(data)==0):
            return 0
        try:
            ids = data[0] # data is a list.
            id_list = ids.split() # ids is a space separated string
            print(id_list)
            latest_email_id = id_list[-1] # get the latest
            print(latest_email_id)
            result, data = self.obj.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822)             for the given ID
            raw_email = str(data[0][1])
        except:
            return 0
        try:
            if email_in_question in raw_email:
                print("yes")
                return 1
            else:
                return 0
        except:
            return 0
        
    def bounce_res_by_gmail(self, email_in_question):
        time.sleep(10)
        self.obj.select()
        result, data = self.obj.search(None, f'(FROM "Mail Delivery Subsystem" SUBJECT "Delivery Status Notification (Failure)")' )
        if len(data)==0:
            return 0
        try:
            ids = data[0] # data is a list.
            id_list = ids.split() # ids is a space separated string
            print(id_list)
            latest_email_id = id_list[-1] # get the latest
            print(latest_email_id)
            result, data = self.obj.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822)             for the given ID
            raw_email = str(data[0][1])
        except:
            return 0
        try:
            if email_in_question in raw_email:
                print("yes")
                return 1
            else:
                return 0
        except:
            return 0

    def is_email_bounced(self, email):
        return self.bounce_res_by_gmail(email) or self.bounce_res_by_postman(email)

# -*- coding: UTF8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


class SMTPMail:
    smtp_server = 'smtp.126.com'
    from_mail = ''
    to_mail = ''
    subject = ''
    message = ''
    attach = ''

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __attach_file(self, attach):
        attach_obj = MIMEImage(file(attach, 'rb').read())
        attach_obj['Content-Type'] = 'application/octet-stream'
        attach_obj.add_header('content-disposition', 'attachment', filename=attach)
        return attach_obj

    def send(self):
        msg = MIMEMultipart()
        msg['From'] = self.from_mail
        msg['To'] = self.to_mail
        msg['Subject'] = self.subject

        content = MIMEText(self.message, 'html')
        msg.attach(content)

        if self.attach:
            msg.attach(self.__attach_file(self.attach))

        server = smtplib.SMTP(self.smtp_server)
        server.docmd('ehlo', self.username)
        server.login(self.username, self.password)
        server.sendmail(self.from_mail, self.to_mail, msg.as_string())
        return server.quit()

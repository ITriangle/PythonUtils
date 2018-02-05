#!/bin/env python
# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(subject='邮件主题', message='邮件内容'):
    SMTP_HOST = 'smtp.163.com'
    SMTP_PORT = 25

    FROM = 'fasdfasdfawefaw@163.com'
    PASS = 'fasfas'
    TO = ['python_utils@triangle.com']

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = FROM
    msg['To'] = ';'.join(TO)
    msg['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    smtp.login(FROM, PASS)
    smtp.sendmail(FROM, TO, msg.as_string())
    smtp.quit()


def main():
    send_email()


if __name__ == '__main__':
    main()

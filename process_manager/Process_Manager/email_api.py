# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives

text_content = u'This is a message'
form_email = 'oprobot@mftour.cn'

def send_email(subject,to,html_content):
    if(len(to) > 0):
        msg = EmailMultiAlternatives(subject, text_content, form_email, to)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
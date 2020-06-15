from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage


def send_email(subject, from_email, recipient_list, text_template, html_template=None, attachments=None):
    
    pass
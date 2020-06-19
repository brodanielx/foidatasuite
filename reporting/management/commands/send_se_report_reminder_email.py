from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from core.send_email import send_email


class Command(BaseCommand):

    help = 'Send reminder email to complete weekly self-examination report.'

    def handle(self, *args, **kwargs):

        subject = 'Reminder: Weekly FOI Self-Examination Report'

        recipient_list = ['dnilssoncole@gmail.com']

        text_content = render_to_string('email/email_ref.txt')
        html_content = render_to_string('email/se_report_reminder.html')

        send_email(
            subject,
            recipient_list,
            text_content,
            html_content
        )

       
        # finish weekly reminder email - add form link to buttone
        # create .txt templates for all emails

        
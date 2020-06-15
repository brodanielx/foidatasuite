

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from email.mime.image import MIMEImage



class Command(BaseCommand):

    help = 'Send reminder email to complete weekly self-examination report.'

    def handle(self, *args, **kwargs):

        subject = 'Subject: Testing django email!!'
        
        from_email = 'baiisdemo@gmail.com'
        recipient_list = ['bro.danielx@gmail.com']

        text_content = render_to_string('email/email_ref.txt')
        html_content = render_to_string('email/email_ref.html')

        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            recipient_list,
        )

        msg.attach_alternative(html_content, "text/html")
        msg.mixed_subtype = 'related'

        msg.send()

        # add code to send_email.py
        # embedd and attach images
        # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/

        
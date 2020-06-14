

from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template



class Command(BaseCommand):

    help = 'Send reminder email to complete weekly self-examination report.'

    def handle(self, *args, **kwargs):

        # email html templates: https://colorlib.com/wp/responsive-html-email-templates/

        # get FOI that have not completed report
        # create email html and plain text templates
        # send email

        # test email

        subject = 'Subject: Testing django email!!'
        message = 'this is the message'
        # html_message = '<h1>This is html!</h1>'
        from_email = 'baiisdemo@gmail.com'
        recipient_list = ['bro.danielx@gmail.com']

        html_message = get_template('email/email_ref.html').render()

        send_mail(
            subject, 
            message, 
            from_email, 
            recipient_list,
            html_message=html_message,
            fail_silently=True
        )

        # use EmailMultiAlternatives for embedding images in email. 
        # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/

        
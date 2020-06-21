from datetime import datetime
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from core.send_email import send_email
from foidata.data.se_report_completed import SEReportCompleted


class Command(BaseCommand):

    help = 'Send reminder email to complete weekly self-examination report.'

    def handle(self, *args, **kwargs):

        data = SEReportCompleted()
        profiles = list(data.foi_not_completed())

        print('> Sending weekly self-examination report reminder emails...')
        for profile in profiles:
            self.render_email(profile)
            print(f' - {profile}')
       
        
        # set up foitampa.automate@gmail.com for app emails
        # set up logging - https://docs.djangoproject.com/en/3.0/topics/logging/
        # resolve security messages from git bot

    def render_email(self, profile):
        today_str = datetime.now().strftime('%m/%d/%Y')
        subject = f'Reminder: Weekly FOI Self-Examination Report {today_str}'

        recipient_list = [profile.user.email]
        context = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'nation_id': profile.nation_id
        }

        text_content = render_to_string('email/se_report_reminder.txt', context)
        html_content = render_to_string('email/se_report_reminder.html', context)

        send_email(
            subject,
            recipient_list,
            text_content,
            html_content
        )

        pass

        
import logging
from datetime import datetime
from email.mime.image import MIMEImage

from django.core import management
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from core.send_email import send_email
from foidata.data.se_report import SelfExaminationReport
from users.models import Profile

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Send email with se data to inidividual FOI.'

    def handle(self, *args, **kwargs):
        management.call_command('update_data_csv')

        self.data = SelfExaminationReport()
        profiles = Profile.objects.receive_emails()

        for profile in profiles:
            self.render_email(profile)

    
    def render_email(self, profile):
        nation_id = profile.nation_id

        context = self.data.individual_last_two_weeks(nation_id)
        context['full_name'] = f'{profile.user.first_name} {profile.user.last_name}'
        context['nation_id'] = profile.nation_id

        end = context['end'].strftime('%m/%d/%Y')
        
        subject = f'Weekly FOI Self-Examination {end}'

        recipient_list = [profile.user.email]

        text_content = render_to_string('email/weekly_individual_stats.txt', context)
        html_content = render_to_string('email/weekly_individual_stats.html', context)
        
        try:
            send_email(
                subject,
                recipient_list,
                text_content,
                html_content
            )
        except:
            logger.exception(f'An error occurred while sending email to {recipient_list} with the subject: {subject}')

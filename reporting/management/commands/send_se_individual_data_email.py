import logging
from datetime import datetime
from email.mime.image import MIMEImage

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

        self.data = SelfExaminationReport()
        profiles = Profile.objects.receive_emails()

        for profile in profiles:
            self.render_email(profile)

    
    def render_email(self, profile):
        nation_id = profile.nation_id

        context = self.data.individual_last_two_weeks(nation_id)
        

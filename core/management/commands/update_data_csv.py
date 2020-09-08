import logging
import os

from django.core import management
from django.core.management.base import BaseCommand, CommandError

from foidata.service.constants import CSV_DIRECTORY
from foidata.service.googlesheets import GoogleSheetsToCSVService

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Updates .csv files with most recent FOI data.'


    def handle(self, *args, **kwargs):

        svc = GoogleSheetsToCSVService()

        try:

            self.stdout.write(' - Collecting Dues...')
            svc.dues()

            self.stdout.write(' - Collecting FCN...')
            svc.fcn()

            self.stdout.write(' - Collecting FOI Class Attendance...')
            svc.foi_class_attendance()

            self.stdout.write(' - Collecting Roster...')
            svc.roster()

            self.stdout.write(' - Collecting Self-Examination...')
            svc.self_examination()

            management.call_command('create_update_users')

            self.stdout.write(self.style.SUCCESS('Done!'))

        except Exception as e:
            logger.error(e)
            raise CommandError('An error occurred.')
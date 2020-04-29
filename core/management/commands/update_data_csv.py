import os

from django.core.management.base import BaseCommand, CommandError

from foidata.service.constants import CSV_DIRECTORY
from foidata.service.googlesheets import GoogleSheetsToCSVService


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

            self.stdout.write(self.style.SUCCESS('Done!'))

        except:
            raise CommandError('An error occurred.')
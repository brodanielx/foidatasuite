

from django.core.management.base import BaseCommand, CommandError

from foidata.service.googlesheets import GoogleSheetsToCSVService


class Command(BaseCommand):

    help = 'Updates .csv files with most recent FOI data.'


    def handle(self, *args, **kwargs):

        svc = GoogleSheetsToCSVService()

        # check that the path foidata/csv exists, if it does not exist, create it

        svc.dues()
        svc.fcn()
        svc.foi_class_attendance()
        svc.roster()
        svc.self_examination()
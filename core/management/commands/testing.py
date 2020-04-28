import os

from django.core.management.base import BaseCommand

from foidata.data.data import FOIData


class Command(BaseCommand):

    help = 'for debugging purposes only.'


    def handle(self, *args, **kwargs):

        data = FOIData()
        print(data.foi_class_attendance.tail())
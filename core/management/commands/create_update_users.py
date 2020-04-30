import os

from django.core.management.base import BaseCommand

from users.utils import UserUtils


class Command(BaseCommand):

    help = 'Create or update FOI models from FOIRoster google sheet.'


    def handle(self, *args, **kwargs):

        utils = UserUtils()
        
        created_count, updated_count = utils.create_or_update()

        self.stdout.write(self.style.SUCCESS(
            f'{created_count} FOI created. {updated_count} FOI Updated.'
        ))
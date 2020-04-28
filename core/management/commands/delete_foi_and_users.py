import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from foi.models import FOI


class Command(BaseCommand):

    help = 'Delete all FOI and Users.'


    def handle(self, *args, **kwargs):

        foi_count = FOI.objects.filter(user__is_superuser=False).count()
        user_count = User.objects.filter(is_superuser=False).count()
        FOI.objects.filter(user__is_superuser=False).delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.SUCCESS(
            f'{foi_count} FOI and {user_count} Users deleted.'
        ))
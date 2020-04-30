import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from users.models import Profile


class Command(BaseCommand):

    help = 'Delete all Profiles and Users for non superusers.'


    def handle(self, *args, **kwargs):

        profile_count = Profile.objects.filter(user__is_superuser=False).count()
        user_count = User.objects.filter(is_superuser=False).count()
        Profile.objects.filter(user__is_superuser=False).delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.SUCCESS(
            f'{profile_count} Profiles and {user_count} Users deleted.'
        ))
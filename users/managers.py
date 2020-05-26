from django.db import models

class ProfileManager(models.Manager):

    def active(self):
        queryset = self.get_queryset()
        profiles = queryset.filter(user__is_active=True)
        return profiles

    def inactive(self):
        queryset = self.get_queryset()
        profiles = queryset.filter(user__is_active=False)
        return profiles
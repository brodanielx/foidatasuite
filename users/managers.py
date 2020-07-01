from django.db import models

class ProfileManager(models.Manager):

    def active(self):
        queryset = self.get_queryset()
        return queryset.filter(user__is_active=True)

    def inactive(self):
        queryset = self.get_queryset()
        return queryset.filter(user__is_active=False)

    def receive_emails(self):
        queryset = self.active()
        return queryset.filter(receive_emails=True)
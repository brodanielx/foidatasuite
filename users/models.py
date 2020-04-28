
from django.contrib.auth.models import User
from django.db import models
from PIL import Image

from foidata_proj.settings.constants import MAX_IMAGE_HEIGHT

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    nation_id = models.IntegerField(null=True)
    city = models.CharField(max_length=100)
    rank = models.CharField(max_length=100)
    receive_emails = models.BooleanField(default=False)

    def __str__(self):
        return f'Profile: {self.nation_id} - {self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > MAX_IMAGE_HEIGHT or img.width > MAX_IMAGE_HEIGHT:
            output_size = (MAX_IMAGE_HEIGHT, MAX_IMAGE_HEIGHT)
            img.thumbnail(output_size)
            img.save(self.image.path)

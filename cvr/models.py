from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import smart_str
import os



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/cvs/<filename>
    return 'cvs/{}'.format(filename)

def user_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/<filename>
    return 'images/{}'.format(filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to=user_image_path, blank=True)
    cv = models.FileField(upload_to=user_directory_path, blank=True)
    free_text = models.CharField(max_length=200, blank=True)

    def filename(self):
        return os.path.basename(self.cv.name)

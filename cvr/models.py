from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django_resized import ResizedImageField

import traceback
import os
from PIL import Image, ExifTags



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
    image = ResizedImageField(upload_to=user_image_path, blank=True)
    cv = models.FileField(upload_to=user_directory_path, blank=True)
    free_text = models.CharField(max_length=500, blank=True)
    is_approved = models.BooleanField(default=False)
    is_privledged = models.BooleanField(default=False)
        
    def filename(self):
        return os.path.basename(self.cv.name)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if self.image:
            try:
                image=Image.open(self.image)
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation]=='Orientation': break
                exif=dict(image._getexif().items())
                if   exif[orientation] == 3:
                    image=image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image=image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image=image.rotate(90, expand=True)
                image.save(self.image.path)
            except:
                traceback.print_exc()

    def __str__(self):
        return "(ID={}) {} {} - is{} approved".format(self.id, self.first_name, self.last_name, "" if self.is_approved else " not")
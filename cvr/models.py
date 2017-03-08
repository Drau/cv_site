from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/csv/<filename>
    return 'cvs/{}'.format(filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    cv = models.FileField(upload_to=user_directory_path)
    free_text = models.CharField(max_length=200)

from django.db import models
from django.contrib.auth.models import User

import uuid
import os

class UserModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    joined_on = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


def path_and_rename(instance, filename):
    upload_to = instance.user.id
    ext = filename.split('.')[-1]

    filename = '{}.{}'.format(str(instance.pk), str(ext))
        
    return os.path.join(str(upload_to),str(filename))
    

class PhotoModel(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE,null=False,blank=False)
    photo = models.ImageField(upload_to=path_and_rename,null=True,blank=True)

    def __str__(self):
        return str(self.user)
from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from authentication.models import User

# Create your models here.


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    

class File(models.Model):
    # name = models.CharField(max_length=50)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', storage=MediaCloudinaryStorage())
    file = models.FileField(upload_to='files/')
    created = models.DateTimeField(auto_now_add=True)

from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from authentication.models import User

# Create your models here.


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Folder Case {"0"*min(0, len(3-str(self.id)))+str(self.id)} {self.user.email}'
    

class Thumbnail(models.Model):
    ext = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to='thumbnails/', storage=MediaCloudinaryStorage())
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Thumbnail {self.image.name[-10:]}...{self.ext}'



class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    thumbnail = models.ForeignKey(Thumbnail, on_delete=models.CASCADE, null=True)
    # thumbnail = models.ImageField(upload_to='thumbnails/', storage=MediaCloudinaryStorage())
    file = models.FileField(upload_to='files/')
    file_content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'File Case {"0"*min(0, len(3-str(self.id)))+str(self.id)}'

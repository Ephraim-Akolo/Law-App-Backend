from django.db import models
from authentication.models import User

# Create your models here.


class ChatGPTPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class LamaPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    

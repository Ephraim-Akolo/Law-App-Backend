from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.ChatGPTPrompt)
admin.site.register(models.LamaPrompt)

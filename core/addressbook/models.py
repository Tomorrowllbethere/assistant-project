from django.db import models
import random
from core import settings
import cloudinary
from cloud.models import MediaFile

class AllContact(models.Model):
    fullname = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50)
    birthday = models.DateField()
    host_id = models.IntegerField(null=False)
   
    # Поле для збереження завантаженого аватара або вибраного з Cloudinary
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Додаткове поле для збереження URL до стандартного аватара
    avatar_url = models.URLField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Якщо користувач вибрав аватар з Cloudinary
        if not self.avatar and not self.avatar_url:
            self.avatar_url = settings.DEFAULT_AVATARS['neutral']  # Задаємо стандартний аватар за замовчуванням
        super().save(*args, **kwargs)

    def get_avatar_url(self):
        if self.avatar_url:
            return self.avatar_url  # Якщо користувач вибрав аватар з Cloudinary
        elif self.avatar:
            return self.avatar.url  # Якщо користувач завантажив власне зображення
        return settings.DEFAULT_AVATARS['neutral']  # Повертаємо стандартний аватар

class Phone(models.Model):
    ntel = models.CharField(max_length=10)
    contactp = models.ForeignKey(AllContact, related_name='phones', on_delete=models.CASCADE)

    def __str__(self):
        return self.ntel
    
class Email(models.Model):
    mail = models.CharField(max_length=30)
    contacte = models.ForeignKey(AllContact, related_name='emails', on_delete=models.CASCADE)

    def __str__(self):
        return self.mail
    



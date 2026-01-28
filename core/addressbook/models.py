from django.db import models
import random
from core import settings
import cloudinary
from cloud.models import MediaFile

class AllContact(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        NEUTRAL = 'N', 'Neutral'


    fullname = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50)
    birthday = models.DateField()
    host_id = models.IntegerField(null=False)
    
    gender = models.CharField(
        max_length=1, 
        choices=Gender.choices, 
        default=Gender.NEUTRAL
    )
   
    # Поле для збереження завантаженого аватара або вибраного з Cloudinary
    avatar = cloudinary.models.CloudinaryField('image', folder='contacts_avatars', blank=True, null=True)    
    # Додаткове поле для збереження URL до стандартного аватара
    avatar_url = models.URLField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Якщо користувач вибрав аватар з Cloudinary
        if not self.avatar and not self.avatar_url:
            self.avatar_url= settings.DEFAULT_AVATARS.get(self.gender) # Задаємо стандартний аватар за замовчуванням
        super().save(*args, **kwargs)

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url  # Якщо користувач вибрав аватар з Cloudinary
        elif self.avatar_url:
            return self.avatar_url  # Якщо користувач завантажив власне зображення
        return settings.DEFAULT_AVATARS.get(self.gender, settings.DEFAULT_AVATARS['N'])
    def __str__(self):
        return self.fullname

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
    



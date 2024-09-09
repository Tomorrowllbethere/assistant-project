from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from contextlib import contextmanager
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        if instance.is_superuser:
            return    
        if created and not instance.is_superuser:
            Profile.objects.create(user=instance)     
    except Exception as e:
        print(f' It was error is signals: {e}')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    




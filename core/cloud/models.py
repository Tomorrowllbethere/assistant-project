
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} (User: {self.user.username})'


class MediaFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name="files")
    file = CloudinaryField(folder=lambda instance: f'user_{instance.user.id}/{instance.folder.name}' if instance.folder else f'user_{instance.user.id}')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def move_to_folder(self, new_folder):
        if new_folder.user != self.user:
            raise ValueError("You can only move files to your own folders.")
        self.folder = new_folder
        self.save()

    def __str__(self):
        return f'{self.file.public_id} (Folder: {self.folder.name if self.folder else "No Folder"})'

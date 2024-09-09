
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class MediaFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = CloudinaryField(resource_type='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=20, default="raw")

    def __str__(self):
        return self.file.public_id

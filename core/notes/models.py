from django.db import models
from django.contrib.auth.models import User

class NoteList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notebooks')
    list_name = models.CharField(max_length=255)

    def __str__(self):
        return self.list_name

class Tag(models.Model):
    tag = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.tag

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    expire_at = models.DurationField(null=True, blank=True)
    
    notebook = models.ForeignKey(NoteList, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    tag = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tag


class NoteList(models.Model):
    list_name = models.CharField(max_length= 225, default='Default Notebook')
    
    def __str__(self):
        return self.list_name
    
class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default = False)

    start_date = models.DateTimeField(null= True, default = timezone.now)
    end_date= models.DateTimeField(null= True)
    tags = models.ManyToManyField(Tag, related_name='note', blank=True)
    notebook = models.ForeignKey(NoteList, related_name='notebook', on_delete=models.CASCADE,  default='1')

    def __str__(self):
        return self.title

    

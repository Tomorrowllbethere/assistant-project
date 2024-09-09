from django.db import models

class AllContact(models.Model):
    fullname = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50)
    birthday = models.DateField()
    host_id = models.IntegerField(null=False)

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

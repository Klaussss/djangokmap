from django.db import models

# Create your models here.

# Database for saving the file
class Folder(models.Model):
    username = models.CharField(max_length=200,default="NULL")
    filename = models.CharField(max_length=1000,default="NULL")
    #filepath = models.FileField(upload_to = "./folder")
    filepath = models.CharField(max_length=400,default="NULL")
    def __unicode__(self):
        return self.file;

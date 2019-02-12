from django.db import models

# Create your models here.
class AccountInfo(models.Model):
    username        = models.CharField(max_length=100);
    password        = models.CharField(max_length=100);
    chinesename     = models.CharField(max_length=100,default="NULL");
    researchtopic   = models.CharField(max_length=100,default="NULL");
    grade           = models.CharField(max_length=100,default="NULL");
    hometown        = models.CharField(max_length=100,default="NULL");
    phonenumber     = models.CharField(max_length=100,default="NULL");
    email           = models.CharField(max_length=100,default="NULL");

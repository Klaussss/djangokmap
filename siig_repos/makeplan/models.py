from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class Plans(models.Model):
    username = models.CharField(max_length=100);
    planid = models.CharField(max_length=150,default="default");
    datetime = models.CharField(max_length=100,default=timezone.now); 
    plan1 = models.CharField(max_length=500,default="NULL");
    plan2 = models.CharField(max_length=500,default="NULL");
    plan3 = models.CharField(max_length=500,default="NULL");
    plan4 = models.CharField(max_length=500,default="NULL");
    plan5 = models.CharField(max_length=500,default="NULL");
    plan6 = models.CharField(max_length=500,default="NULL");
    plan7 = models.CharField(max_length=500,default="NULL");
    summary1 = models.CharField(max_length=500,default="NULL");
    summary2 = models.CharField(max_length=500,default="NULL");
    summary3 = models.CharField(max_length=500,default="NULL");
    summary4 = models.CharField(max_length=500,default="NULL");
    summary5 = models.CharField(max_length=500,default="NULL");
    summary6 = models.CharField(max_length=500,default="NULL");
    summary7 = models.CharField(max_length=500,default="NULL");
    shareto = models.CharField(max_length=500,default="NULL");
    submitto = models.CharField(max_length=500,default="NULL");

class Comment(models.Model):
    username = models.CharField(max_length=100,default="NULL")
    commenter = models.CharField(max_length=100,default="NULL")
    planid = models.CharField(max_length=150,default="NULL")
    content = models.CharField(max_length=500,default="NULL")
    datetime = models.DateTimeField(max_length=100,default=timezone.now); 

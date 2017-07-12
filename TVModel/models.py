# encoding: utf-8
from django.db import models

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=500)

class Program(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    url = models.CharField(max_length=500)

class ProgramDetail(models.Model):
    name = models.CharField(max_length=20)
    menu = models.TextField()
    address = models.TextField()

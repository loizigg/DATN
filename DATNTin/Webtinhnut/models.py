from django.db import models

# Create your models here.
class Tinhnut(models.Model):
    name = models.CharField(max_length=10)
    b = models.FloatField()
    h = models.FloatField()
    L = models.FloatField()
    cben= models.CharField()
    nthep= models.CharField()
    thepd= models.CharField()
    a = models.FloatField()
    thept= models.CharField()
    a1 = models.FloatField()

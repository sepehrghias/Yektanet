from django.db import models

# Create your models here.

class Advertiser(models.Model):
    advertiser_name = models.CharField(max_length=200)
    number_of_advertisements = models.IntegerField(default=0)

class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    content = models.TextField()
    priority = models.IntegerField(default=0)

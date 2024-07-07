from django.db import models


# Create your models here.

class Advertiser(models.Model):
    advertiser_name = models.CharField(max_length=200)


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    content = models.TextField()
    click = models.IntegerField(default=0)
    image = models.ImageField(upload_to='ads/')
    views = models.IntegerField(default=0)

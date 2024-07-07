from django.db import models


# Create your models here.

class Advertiser(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Ad(models.Model):
    advertiser = models.ForeignKey("advertiser_management.Advertiser", on_delete=models.CASCADE , related_name="ads")
    title = models.TextField()
    click = models.IntegerField(default=0)
    image = models.ImageField(upload_to='ads/')
    views = models.IntegerField(default=0)
    landing_url = models.URLField(max_length=200)
    def __str__(self):
        return self.title
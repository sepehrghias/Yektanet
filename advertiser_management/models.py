from django.db import models


# Create your models here.

class Advertiser(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Ad(models.Model):
    advertiser = models.ForeignKey("advertiser_management.Advertiser", on_delete=models.CASCADE, related_name="ads")
    title = models.TextField()
    image = models.ImageField(upload_to='ads/')
    landing_url = models.URLField(max_length=200)
    approve = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Click(models.Model):
    ad = models.ForeignKey("advertiser_management.Ad", on_delete=models.CASCADE, related_name="clicks")
    click_date = models.DateTimeField("click date")
    ip_address = models.GenericIPAddressField()

class View(models.Model):
    ad = models.ForeignKey("advertiser_management.Ad", on_delete=models.CASCADE, related_name="views")
    view_date = models.DateTimeField("view date")
    ip_address = models.GenericIPAddressField()


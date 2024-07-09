from django.urls import path
from advertiser_management import views
from advertiser_management.views import AdvertiserList
app_name = 'advertiser_management'
urlpatterns = [
    path("", AdvertiserList.as_view(), name="index"),
    path("create/", views.create_ad, name="create_ad"),
    path("<int:ad_id>/", views.click, name="click"),

]
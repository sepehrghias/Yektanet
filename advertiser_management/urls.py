from django.urls import path
from . import views
app_name = 'advertiser_management'
urlpatterns = [
    path("", views.index, name="index"),
    path("make/<int:advertiser_id>/", views.make_ad, name="make_ad"),
    path("<int:ad_id>/", views.click, name="click"),

]
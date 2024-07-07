from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("make/", views.make_ad, name="make_ad"),
    path("<int:ad_id>/", views.click, name="click"),

]
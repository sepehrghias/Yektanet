from django.urls import path
from advertiser_management import views
app_name = 'advertiser_management'
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_ad, name="create_ad"),
    path("<int:ad_id>/", views.click, name="click"),

]
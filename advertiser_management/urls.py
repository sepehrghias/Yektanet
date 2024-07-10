from django.urls import path
from advertiser_management import views
from advertiser_management.views import AdvertiserList , CreatingForm
app_name = 'advertiser_management'
urlpatterns = [
    path("", AdvertiserList.as_view(), name="index"),
    path("create/", CreatingForm.as_view(), name="create_ad"),
    path("<int:ad_id>/", views.click, name="click"),
    path("report/", views.report,name="report"),
]
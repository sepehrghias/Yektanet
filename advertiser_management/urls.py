from django.urls import path
from advertiser_management.views import AdvertiserListView, AdListView, AdReportView,ClickCreateView
app_name = 'advertiser_management'
urlpatterns = [
    path("", AdvertiserListView.as_view(), name="index"),
    path("create/", AdListView.as_view(), name="create_ad"),
    path("<int:ad_id>/", ClickCreateView.as_view(), name="click"),
    path("report/", AdReportView.as_view(), name="report"),
]
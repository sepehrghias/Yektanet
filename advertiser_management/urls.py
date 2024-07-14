from django.urls import path
from advertiser_management.views import AdvertiserListView, AdListView, AdReportView,ClickCreateView, AdGoCpc
app_name = 'advertiser_management'
urlpatterns = [
    path("", AdvertiserListView.as_view(), name="index"),
    path("create/", AdListView.as_view({'get': 'list' , "post" : 'create'}), name="create_ad"),
    path("<int:ad_id>/", ClickCreateView.as_view(), name="click"),
    path("report/", AdReportView.as_view(), name="report"),
    path("min_cpc/", AdGoCpc.as_view(), name="min_cpc"),
]
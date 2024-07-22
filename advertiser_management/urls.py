from django.urls import path
from advertiser_management.views import AdList, AdView, AdReportView, ClickView
app_name = 'advertiser_management'
urlpatterns = [
    path("", AdList.as_view(), name="index"),
    path("create/", AdView.as_view(), name="create_ad"),
    path("<int:ad_id>/", ClickView.as_view(), name="click"),
    path("report/", AdReportView.as_view(), name="report"),
]
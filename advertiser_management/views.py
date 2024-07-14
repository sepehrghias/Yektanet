from django.utils import timezone
from django.db import transaction
from django.db.models import Count, ExpressionWrapper, Avg, F, fields
from django.db.models.functions import TruncHour
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ViewSet

from advertiser_management.models import Advertiser, Ad, View, Click
from advertiser_management.serializers import AdSerializer, AdvertiserSerializer, AdGetterSerializer


class AdvertiserListView(generics.ListCreateAPIView):
    queryset = Advertiser.objects.all()
    serializer_class = AdvertiserSerializer
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        for advertiser in self.get_queryset():
            for ad in advertiser.ads.all():
                View.objects.create(ad=ad, view_date=timezone.now(), ip_address=request.ip)
        return response

@permission_classes([IsAuthenticated, IsAdminUser])
class AdListView(ViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def list(self, request, *args, **kwargs):
        return Response()
    def create(self, request, *args, **kwargs):
        serializer = AdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClickCreateView(APIView):
    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, pk=ad_id)
        Click.objects.create(ad=ad, click_date=timezone.now(), ip_address=request.ip)
        return Response({'url': ad.landing_url}, status=302)

@permission_classes([IsAuthenticated, IsAdminUser])
class AdReportView(APIView):
    def get(self, request):
        ads = Ad.objects.all()
        report = []

        for ad in ads:
            clicks_per_hour = Click.objects.filter(ad=ad).annotate(hour=TruncHour('click_date')).values('hour').annotate(click_count=Count('id')).order_by('hour')
            views_per_hour = View.objects.filter(ad=ad).annotate(hour=TruncHour('view_date')).values('hour').annotate(view_count=Count('id')).order_by('hour')

            total_clicks = Click.objects.filter(ad=ad).count()
            total_views = View.objects.filter(ad=ad).count()
            ctr = (total_clicks / total_views) if total_views > 0 else 0

            avg_time_diff = Click.objects.filter(ad=ad).annotate(time_diff=ExpressionWrapper(F('click_date') - F('ad__views__view_date'), output_field=fields.DurationField())).aggregate(Avg('time_diff'))

            clicks_dict = {item['hour']: item['click_count'] for item in clicks_per_hour}
            views_dict = {item['hour']: item['view_count'] for item in views_per_hour}

            ctr_per_hour = []
            all_hours = sorted(set(clicks_dict.keys()).union(set(views_dict.keys())))
            for hour in all_hours:
                hour_clicks = clicks_dict.get(hour, 0)
                hour_views = views_dict.get(hour, 0)
                hour_ctr = (hour_clicks / hour_views) if hour_views > 0 else 0
                ctr_per_hour.append({
                    'hour': hour,
                    'clicks': hour_clicks,
                    'views': hour_views,
                    'ctr': hour_ctr,
                })

            report.append({
                'ad': AdSerializer(ad).data,
                'total_clicks': total_clicks,
                'total_views': total_views,
                'clicks_per_hour': clicks_per_hour,
                'views_per_hour': views_per_hour,
                'ctr': ctr,
                'avg_time_diff': avg_time_diff['time_diff__avg'],
                'ctr_per_hour': ctr_per_hour,
            })

        return Response(report)

class AdGoCpc(APIView):
    def get(self, request):
        sorted_ads = Ad.objects.all().order_by('-cpc').values()
        serilizer = AdGetterSerializer(sorted_ads, many=True)
        return Response(serilizer.data)
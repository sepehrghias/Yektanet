from django.utils import timezone
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse ,reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.db.models import Count, ExpressionWrapper , Avg, F , fields
from django.db.models.functions import TruncHour
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from advertiser_management.forms import CreateAdForm
from advertiser_management.models import Advertiser, Ad , View , Click


class AdvertiserList(ListView):
    model = Advertiser
    template_name = 'advertiser_management/ads.html'
    context_object_name = 'advertisers'
    @transaction.atomic
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for advertiser in context['advertisers']:
            for ad in advertiser.ads.all():
                View.objects.create(
                    ad=ad,
                    view_date=timezone.now(),
                    ip_address=self.request.ip
                )
        return context

class CreatingForm(CreateView):
    template_name = 'advertiser_management/create_ad_form.html'
    form_class = CreateAdForm
    success_url = reverse_lazy('advertiser_management:index')

def click(request , ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    Click.objects.create(ad=ad, click_date=timezone.now(), ip_address=request.ip)
    return redirect(ad.landing_url)

class AdReportView(ListView):
    model = Ad
    template_name = 'advertiser_management/report.html'
    context_object_name = 'ads'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ads = context['ads']
        report = []

        for ad in ads:
            # Get clicks per hour
            clicks_per_hour = Click.objects.filter(ad=ad).annotate(
                hour=TruncHour('click_date')
            ).values('hour').annotate(click_count=Count('id')).order_by('hour')

            # Get views per hour
            views_per_hour = View.objects.filter(ad=ad).annotate(
                hour=TruncHour('view_date')
            ).values('hour').annotate(view_count=Count('id')).order_by('hour')

            total_clicks = Click.objects.filter(ad=ad).count()
            total_views = View.objects.filter(ad=ad).count()
            ctr = (total_clicks / total_views) if total_views > 0 else 0

            avg_time_diff = Click.objects.filter(ad=ad).annotate(
                time_diff=ExpressionWrapper(
                    F('click_date') - F('ad__views__view_date'), output_field=fields.DurationField()
                )
            ).aggregate(Avg('time_diff'))

            # Create a dictionary for easier lookup
            clicks_dict = {item['hour']: item['click_count'] for item in clicks_per_hour}
            views_dict = {item['hour']: item['view_count'] for item in views_per_hour}

            # Calculate CTR per hour
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
                'ad': ad,
                'total_clicks': total_clicks,
                'total_views': total_views,
                'clicks_per_hour': clicks_per_hour,
                'views_per_hour': views_per_hour,
                'ctr': ctr,
                'avg_time_diff': avg_time_diff['time_diff__avg'],
                'ctr_per_hour': ctr_per_hour,
            })

        context['report'] = report
        return context
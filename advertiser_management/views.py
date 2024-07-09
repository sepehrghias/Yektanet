from django.utils import timezone
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse ,reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

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
                    ip_address=self.request.META['REMOTE_ADDR']
                )
        return context

class CreatingForm(CreateView):
    model = Ad
    template_name = 'advertiser_management/create_ad_form.html'
    form_class = CreateAdForm
    success_url = reverse_lazy('advertiser_management:index')


    # def create_ad(request):
    #     form = CreateAdForm(request.POST or None, request.FILES or None)
    #     if request.method == "GET":
    #         return render(request, "advertiser_management/create_ad_form.html", context={"form": form})
    #     else:
    #         if form.is_valid():
    #             form.save()
    #             return HttpResponseRedirect(reverse('advertiser_management:index'))
    #         return render(request, "advertiser_management/create_ad_form.html", context={"form": form})

def click(request , ad_id):
    ad = Ad.objects.get(pk=ad_id)
    new_click = Click.objects.create(ad=ad, click_date=timezone.now(), ip_address=request.ip)
    return redirect(ad.landing_url)


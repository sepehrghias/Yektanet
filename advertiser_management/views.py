from django.utils import timezone
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from advertiser_management.forms import CreateAdForm
from advertiser_management.models import Advertiser, Ad, View, Click

@transaction.atomic
def index(request):
    advertisers = Advertiser.objects.all()
    context = {'advertisers': advertisers}
    for advertiser in advertisers:
        for ad in advertiser.ads.all():
            view = View.objects.create(
            ad =ad,
            view_date =timezone.now(),
            ip_address =request.ip
            )
    return render(request, "advertiser_management/ads.html", context)

def create_ad(request):
    form = CreateAdForm(request.POST or None, request.FILES or None)
    if request.method == "GET":
        return render(request, "advertiser_management/create_ad_form.html", context={"form":form})
    else:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('advertiser_management:index'))
        return render(request, "advertiser_management/create_ad_form.html", context={"form":form})

def click(request , ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    Click.objects.create(ad=ad, click_date=timezone.now(), ip_address=request.ip)
    return redirect(ad.landing_url)


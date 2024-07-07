from django.shortcuts import render , redirect
from django.db.models import F
# Create your views here.
from django.http import HttpResponse

from advertiser_management.models import Advertiser , Ad


def index(request):
    advertisers = Advertiser.objects.all()
    context = {'advertisers': advertisers}
    for advertiser in advertisers:
        for ad in advertiser.ads.all():
            ad.views = F('views') + 1
            ad.save()
    return render(request, "advertiser_management/ads.html", context)

def make_ad(request, advertiser_id):
    context = {'advertiser_id': advertiser_id}
    return render(request, f"advertiser_management/makingForm.html", context)

def click(request , ad_id):
    ad = Ad.objects.get(pk=ad_id)
    ad.click = F('click') + 1
    ad.save()
    return redirect(ad.landing_url)

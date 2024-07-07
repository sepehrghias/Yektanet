from django.shortcuts import render , redirect
from django.db.models import F
from django.urls import reverse
# Create your views here.
from django.http import HttpResponseRedirect

from advertiser_management.models import Advertiser, Ad
from django.views.generic.edit import CreateView

def index(request):
    advertisers = Advertiser.objects.all()
    context = {'advertisers': advertisers}
    for advertiser in advertisers:
        for ad in advertiser.ads.all():
            ad.views = F('views') + 1
            ad.save()
    return render(request, "advertiser_management/ads.html", context)

def make_ad(request):
    try:
        advertiser = Advertiser.objects.get(pk=request.POST["ads_id"])
    except:
        return render(request, "advertiser_management/makingForm.html",
                      {"error_message": "This advertiser does not exist."})

    title = request.POST["title"]
    image = request.POST["image"]
    url = request.POST["url"]
    new_ad = {
        "title": title,
        "image": image,
        "landing_url": url,
        "advertiser": advertiser,
    }
    Ad.objects.create(**new_ad)
    return HttpResponseRedirect(reverse("advertiser_management:index"))

def click(request , ad_id):
    ad = Ad.objects.get(pk=ad_id)
    ad.click = F('click') + 1
    ad.save()
    return redirect(ad.landing_url)

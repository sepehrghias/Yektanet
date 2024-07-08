from django.shortcuts import render , redirect
from django.db.models import F
from django.urls import reverse
# Create your views here.
from django.http import HttpResponseRedirect
from django.forms import ModelForm

from advertiser_management.forms import CreateAdForm
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
    form = CreateAdForm(request.POST or None, request.FILES or None)
    if request.method == "GET":
        return render(request, "advertiser_management/create_ad_form.html", context={"form":form})
    else:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('advertiser_management:index'))
        return render(request, "advertiser_management/create_ad_form.html", context={"form":form})

def click(request , ad_id):
    ad = Ad.objects.get(pk=ad_id)
    ad.click = F('click') + 1
    ad.save()
    return redirect(ad.landing_url)


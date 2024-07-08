from django.contrib import admin

from advertiser_management.models import Advertiser, Ad, View , Click

# Register your models here.
admin.site.register(Advertiser)
admin.site.register(Ad)
admin.site.register(View)
admin.site.register(Click)
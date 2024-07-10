from django.contrib import admin

from advertiser_management.models import Advertiser, Ad, View , Click
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_filter = ('approve',)
    search_fields = ('title', )

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    pass

@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    pass

@admin.register(Advertiser)
class AdvertiserAdmin(admin.ModelAdmin):
    pass
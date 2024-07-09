from django.contrib import admin

from advertiser_management.models import Advertiser, Ad, View , Click

class AdAdmin(admin.ModelAdmin):
    list_filter = ('approve' ,)
    search_fields = ('title', )


# Register your models here.
admin.site.register(Advertiser)
admin.site.register(Ad,AdAdmin)
admin.site.register(View)
admin.site.register(Click)
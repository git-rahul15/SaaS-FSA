from django.contrib import admin

# Register your models here.
from .models import Subscriptions, UserSubscriptions, SubscriptionPrice

class SubscriptionsPriceInline(admin.TabularInline):  #can use stackedinline as well
    readonly_fields = ['product_price_id']
    model= SubscriptionPrice
    extra = 0
    can_delete = False #can't delete prices

class SubscriptionsAdmin(admin.ModelAdmin):
    inlines = [SubscriptionsPriceInline]
    list_display = ["name", "active"]
    readonly_fields = ['product_id']
admin.site.register(Subscriptions, SubscriptionsAdmin) #register app in admin panel
admin.site.register(UserSubscriptions)

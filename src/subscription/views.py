from django.shortcuts import render
from subscription.models import SubscriptionPrice

# Create your views here.

def subscriptionPriceView(request):
    qs_featred = SubscriptionPrice.objects.filter(featured = True)
    qs_monthly_plan = SubscriptionPrice.objects.filter(interval = SubscriptionPrice.IntervalChoices.MONTHLY)
    qs_yearly_plan = SubscriptionPrice.objects.filter(interval = SubscriptionPrice.IntervalChoices.YEARLY)

    return render(request, "subscription/subscriptionPrice.html", context={"featured":qs_featred, "monthly":qs_monthly_plan, "yearly":qs_yearly_plan})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from subscription.models import SubscriptionPrice

# Create your views here.

def product_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session['checkout_subscription_price_id'] = price_id 
    return redirect("stripe-checkout")

@login_required
def checkout_redirect_view(request):
    checkout_subscription_price_id = request.session.get("checkout_subscription_price_id")
    try:
        obj = SubscriptionPrice.objects.get(id= checkout_subscription_price_id)
    except:
        return
    if checkout_subscription_price_id is None or obj is None:
        return redirect('pricing')
    customer_stripe_id = request.user.customers.stripe_id
    return redirect("stripe-end")


def checkout_finalize_view(request):
    return
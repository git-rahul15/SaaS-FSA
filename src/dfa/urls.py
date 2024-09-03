"""
URL configuration for dfa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from auth import views as auth_views
from subscription import views as subscription_views
from checkouts import views as checkout_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('home/', views.home_page_view, name='home'),
    path("pricing/", subscription_views.subscriptionPriceView, name="pricing"),
    path("",views.home_page_view, name='main'),
    path("login_view/", auth_views.login_view, name="login"),
    path("register/", auth_views.register_view, name='register'),
    path('accounts/', include('allauth.urls')),
    path("staff/", views.staff_user, name="staff"),
    path('profiles/', include('profiles.urls')),
    path("checkout/sub-price/<str:price_id>", checkout_views.product_price_redirect_view, name="sub-price-checkout"),
    path("checkout/start/", checkout_views.checkout_redirect_view, name="stripe-checkout"),
    path("checkout/end/", checkout_views.checkout_finalize_view, name="stripe-end"),

]

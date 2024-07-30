from django.urls import path

from . import views


urlpatterns = [
    path("", views.profile_list_View),
    path("<str:username>/", views.profile_details_view, name="profile_view"),

]
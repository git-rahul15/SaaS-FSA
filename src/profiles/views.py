from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()


@login_required
def profile_list_View(request):
    context = {
        'object_list':User.objects.filter(is_active = True)
    }

    return render(request, 'profiles/list.html', context)


@login_required
def profile_details_view(request, username = None, *args, **kwargs):
    user = request.user

    #<app_label>.view_<model_name>
    #<app_label>.change_<model_name>
    #<app_label>.add_<model_name>
    #<app_label>.delete_<model_name>

    profile_user_obj = get_object_or_404(User, username=username)
    is_me = profile_user_obj==user
    context = {
        'object':profile_user_obj,
        'instance': profile_user_obj,
        'owner': is_me
        }
    return render(request, 'profiles/details.html', context)
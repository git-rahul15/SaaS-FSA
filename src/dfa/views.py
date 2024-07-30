from django.http import HttpResponse
from django.shortcuts import render
from visits.models import Visits
from datetime import datetime
import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings


LOGIN_URL  = settings.LOGIN_URL

@login_required(login_url="/accounts/login")
def home_page_view(request, *args, **kwargs):
    # return HttpResponse ("<h1>Hello World </h1>")
    queryset = Visits.objects.all()
    view_count = queryset.count()
    html_template  = 'home.html'
    context = {
        "view_count": view_count
    }
    ist = pytz.timezone('Asia/Kolkata')
    time = datetime.now(tz=ist)
    path = request.path
    Visits.objects.create(path=path, timestamp = time)
    return render (request, html_template, context)


@staff_member_required(login_url="/accounts/login")
def staff_user(request, *args, **kwargs):
    return render(request, 'staff.html',{})


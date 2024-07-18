from django.http import HttpResponse
from django.shortcuts import render
from visits.models import Visits
from datetime import datetime
import pytz

def home_page_view(request, *args, **kwargs):
    # return HttpResponse ("<h1>Hello World </h1>")
    queryset = Visits.objects.all()
    html_template  = 'home.html'
    context = {
        "title": "This is Rahul"
    }
    ist = pytz.timezone('Asia/Kolkata')
    time = datetime.now(tz=ist)
    path = request.path
    view_count = queryset.count()
    Visits.objects.create(path=path, timestamp = time)
    return render (request, html_template, {"view_count":view_count})
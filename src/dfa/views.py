from django.http import HttpResponse
from django.shortcuts import render
from visits.models import Visits
from datetime import datetime
import pytz

def home_page_view(request, *args, **kwargs):
    # return HttpResponse ("<h1>Hello World </h1>")
    queryset = Visits.objects.all()
    html_template  = 'base.html'
    context = {
        "title": "This is Rahul"
    }
    ist = pytz.timezone('Asia/Kolkata')
    time = datetime.now(ist)
    path = request.path
    print(time)
    Visits.objects.create(path=path, timestamp = time)
    return render (request, html_template, {"queryset":queryset})
import requests
import os

from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting


# def index(request):
#     r = requests.get('http://httpbin.org/status/418')
#     print(r.text)
#     return HttpResponse('<pre>' + r.text + '</pre>')
    # times = int(os.environ.get('TIMES', 3))

def index(request):

    return render(request, 'index.html')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

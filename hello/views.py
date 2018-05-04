import requests
import os
import json

from django.shortcuts import render
from django.http import HttpResponse
from hassle.request import EventResponse

from .models import Greeting

# def index(request):
#     r = requests.get('http://httpbin.org/status/418')
#     print(r.text)
#     return HttpResponse('<pre>' + r.text + '</pre>')
    # times = int(os.environ.get('TIMES', 3))

def index(request):
    return render(request, 'index.html')


def query_sms_response(request):
    # try:
    query = json.loads(request.body)['query']
    response_data = EventResponse(query, None, 1)
    response_dict = {"message": response_data.response, "images": response_data.images}

    # except:
    #     response_dict = {"message": 'something went terribly wrong...'}

    response = json.dumps(response_dict)
    return HttpResponse(response)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

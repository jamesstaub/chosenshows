# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, DetailView
# from django.views.generic import TemplateView
from hassle.request import get_events
from hassle.models import Event

class EventsDetail(DetailView):
    model = Event
    template_name = 'hassle/index.html'

    def post(self, request, *args, **kwargs):
        print(get_events())
        return HttpResponse(status=201)

class EventsList(ListView):
    model = Event
    template_name = 'hassle/events_list.html'
    context_object_name = 'event_list'

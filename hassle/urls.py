from .views import EventsList, EventsDetail
from django.conf.urls import url
from django.views.generic import TemplateView

app_name = 'events'

urlpatterns = [
    url(r'^events/$', EventsList.as_view()),
    url(r'^events/index/$', EventsDetail.as_view(), name='detail'),

]

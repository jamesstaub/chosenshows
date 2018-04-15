from . import views
from django.conf.urls import url
from .views.user_sms_profile import edit_user

urlpatterns = [
    url(r'^$', views.sms_endpoint, name='sms'),
    url(r'^accounts/update/(?P<pk>[\-\w]+)/$', edit_user, name='account_update'),
]

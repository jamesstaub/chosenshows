# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse

from django.contrib.auth.models import User
from sms.models import Sms, UserSmsProfile
from hassle.request import EventResponse

@csrf_exempt
def sms_endpoint(request):
    sms_to, sms_from, sms_body = save_sms_received(request)

    response_body = create_sms_response(sms_to, sms_from, sms_body)

    # Start our TwiML response
    resp = MessagingResponse()

    # Add a text message
    msg = resp.message(response_body)

    # Add a picture message
    # msg.media("https://demo.twilio.com/owl.png")
    return HttpResponse(str(resp))


def save_sms_received(request):
    """
    Parse and store SMS from Twilio.

    Return message body and the number sms was sent to as tuples
    """

    # parse sms request
    if request.POST.keys():
        sms_body = request.POST['Body']
        sms_to = request.POST['To']
        sms_from = request.POST['From']
        sms_raw = str(request.POST)

        user = find_or_create_user(sms_from)

        # store SMS
        Sms.objects.create(
            sms_raw=sms_raw,
            sms_body=sms_body,
            sms_to=sms_to,
            sms_from=sms_from)

        return sms_to, sms_from, sms_body

    return None, None, None,


def find_or_create_user(sms_from):
    find_user = User.objects.filter(username=sms_from)

    if find_user.count():
        user = find_user.first()
    else:
        user = User.objects.create_user(
            username=sms_from,
            password=sms_from,
        )

    user_sms_profile = UserSmsProfile.objects.get(user=user)

    user_sms_profile.sms_number = sms_from
    user_sms_profile.save()

    return user


def create_sms_response(sms_to, sms_from, sms_body):

    send_response_from = sms_to
    send_response_to = sms_from

    response_data = EventResponse(sms_body, send_response_to, 1)

    response_body = response_data.response
    # track messages in database
    Sms.objects.create(
        sms_to = send_response_to,
        sms_from = send_response_from,
        sms_body = response_body,
    )

    return response_body

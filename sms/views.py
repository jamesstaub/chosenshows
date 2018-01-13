# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse

from sms.models import Sms
from hassle.parsers import respond_to_user


@csrf_exempt
def sms_endpoint(request):
    sms_to, sms_from, sms_body = parse_sms_received(request)

    response_body = get_sms_response(sms_to, sms_from, sms_body)

    # Start our TwiML response
    resp = MessagingResponse()

    # Add a text message
    msg = resp.message(response_body)

    # Add a picture message
    # msg.media("https://demo.twilio.com/owl.png")
    print(resp)
    return HttpResponse(str(resp))


def parse_sms_received(request):
    """
    Parse and store SMS from Twilio.

    Return message body and the number sms was sent to as a string of tuples
    """

    # parse sms request
    if request.POST.keys():
        sms_body = request.POST['Body']
        sms_to = request.POST['To']
        sms_from = request.POST['From']
        sms_raw = str(request.POST)

        user, newly_created = find_or_create_user(sms_from)

        # store SMS
        Sms.objects.create(
            sms_raw=sms_raw,
            sms_body=sms_body,
            sms_to=sms_to,
            sms_from=sms_from)

        return sms_to, sms_from, sms_body

    return None, None, None,


def get_sms_response(sms_to, sms_from, sms_body):

    send_response_from = sms_to
    send_response_to = sms_from

    response_body = respond_to_user(sms_body, send_response_to)

    # track messages in database
    Sms.objects.create(
        sms_to = send_response_to,
        sms_from = send_response_from,
        sms_body = response_body,
    )

    return response_body

def find_or_create_user(sms_from):

    ## FIXME: for prototype only!
    user, newly_created = User.objects.get_or_create(
        username=sms_from,
        password=sms_from,
    )

    return user, newly_created
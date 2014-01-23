from django.template import Context, loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from api.models.default import Business, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from api.lib.xmpp_lib import send_push_from_business_to_favs, register_user, send_push_from_business_to_interacted_users, send_message_to_user
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from api import const
import json
from api.lib.device_help import *

@login_required
def get_businesses(request):
    all_businesses = get_unique_business_handles()
    t = loader.get_template('history_businesses.html')
    c = Context({'businesses' : all_businesses})
    response = HttpResponse(t.render(c))
    return response

@login_required
def get_users_for_business(request, business_handle):
    business_xmpp_handle = '%s@zingcredits.com' % (business_handle)
    all_users = get_user_chats_for_business(business_xmpp_handle)
    t = loader.get_template('user_for_business.html')
    c = Context({'users' : all_users, 'business_handle' : business_handle})
    response = HttpResponse(t.render(c))
    return response

@login_required
def send_push_to_users(request, business_handle):
    t = loader.get_template('send_push_to_users.html')
    c = Context({'business_handle' : business_handle})
    response = HttpResponse(t.render(c))
    return response

def ajax_send_push_to_users(request):
    if request.method == 'GET':
        business_handle = request.GET.get('business_handle')
        message = request.GET.get('message')
        message = message.strip()
        #message = '%s %s' % (const.kSTARTING_FAV_WORD, message)
        print 'MESSAGE:' , message.strip()
        send_push_from_business_to_interacted_users(business_handle, message.strip())
        return HttpResponse(True)
    return HttpResponse(False)


@login_required
def chat_logs(request, user_number, business_handle):
    business_xmpp_handle = '%s@zingcredits.com' % (business_handle)
    all_chats = chat_logs_for_business_and_user(business_xmpp_handle, user_number)
    t = loader.get_template('chat_logs.html')
    c = Context({'chats' : all_chats, 'business_handle' : business_handle, 'user_number' : user_number})
    response = HttpResponse(t.render(c))
    return response

@login_required
def unique_users(request):
    all_users = get_unique_user_handles()
    t = loader.get_template('unique_users.html')
    c = Context({'users' : all_users})
    response = HttpResponse(t.render(c))
    return response


@login_required
def user_businesses(request, user_number):
    businesses = get_all_business_for_user(user_number)
    t = loader.get_template('user_businesses.html')
    c = Context({'businesses' : businesses, 'user_number' : user_number})
    response = HttpResponse(t.render(c))
    return response


# TODO: CANT MAKE POST WORK HERE. NEED TO REVISIT
# WHEN I SEND a POST NO DATA COMES THROUGH
def ajax_reply_to_user(request):
    if request.method == 'GET':
        from_business= request.GET.get('from')
        message = request.GET.get('message')
        message = message.strip()
        to_user = request.GET.get('to')
        user = User.objects.get(number = to_user)
        business_handle = '%s@zingcredits.com'  % (from_business)
        business = Business.objects.get(xmpp_handle = business_handle)
        send_message_to_user(business, user, message, should_disconnect=True)
        return HttpResponse(True)
    return HttpResponse(False)

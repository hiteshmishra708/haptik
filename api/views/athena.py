from django.template import Context, loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from api.models.default import Business, User, ChatCollections, ChatMessages, convert_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core import serializers
import json


def index(request):
    all_businesses = Business.objects.filter(active=1).filter(haptik_flag=1).all()
    print 'number of businesses : ', len(all_businesses)
    t = loader.get_template('athena.html')
    c = Context({'businesses' : all_businesses})
    response = HttpResponse(t.render(c))
    return response


def collection_for_business(request, business_id):
    rows = ChatCollections.objects.filter(business_id = business_id).all()
    user_rows = []
    for r in rows:
        a = User.objects.get(id = r.user_id)
        a.coll_id = r.id
        a.from_user = r.from_user
        user_rows.append(a)
    c = Context({'users' : user_rows})
    t = loader.get_template('athena_user_roster.html')
    response = HttpResponse(t.render(c))
    return response

def chats_by_collection(request, coll_id):
    rows = ChatMessages.objects.filter(coll_id=coll_id).all()
    c = Context({'chats' : rows})
    t = loader.get_template('athena_chats.html')
    response = HttpResponse(t.render(c))
    return response


def message_send_from_business(request):
    print '-' * 40
    print request
    body = request.POST.get('body')
    from_user = request.POST.get('from_user')
    if from_user == 'false':
        from_user = False
    else:
        from_user = True
    a = ChatMessages()
    a.coll_id = 1
    a.body = body
    a.direction = from_user
    a.save()
    return HttpResponse(True)


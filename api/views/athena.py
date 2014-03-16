from django.template import Context, loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from api.models.default import Business, User2, ChatCollections, ChatMessaged, convert_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core import serializers
from api.const import *
from api.lib.athena import *
import json


def index(request):
    all_businesses = Business.objects.filter(active=1).filter(haptik_flag=1).all()
    full_list = []
    for b in all_businesses:
        b.unread = get_unread_count_for_business(b.id)
        full_list.append(b)
    full_list= sorted(full_list,key= lambda k:k.unread, reverse=True)
    t = loader.get_template('athena.html')
    c = Context({'businesses' : full_list})
    response = HttpResponse(t.render(c))
    return response


def collection_for_business(request, business_id):
    rows = ChatCollections.objects.filter(business_id = business_id).all()
    business = Business.objects.get(id=business_id)
    print 'business : ', business
    category_id = business.category
    print 'category : ', category_id
    online_agent = None
    if category_id:
        agents = AgentCategory.objects.values_list('agent_id', flat=True).filter(category_id=category_id)
        online_agents = Agents.objects.filter(id__in=agents).filter(online=1)
        if len(online_agents) > 0:
            online_agent = online_agents[0]
    if not online_agent:
        online_agent = Agents.objects.get(id=1)
    agent_name = online_agent.display_name
    print 'agent name : ', agent_name

    user_rows = []
    for r in rows:
        a = User2.objects.get(id = r.user_id)
        a.coll_id = r.id
        a.from_user = r.from_user
        a.unread = r.unread
        user_rows.append(a)
    user_rows = sorted(user_rows,key= lambda k:k.unread, reverse=True)
    c = Context({'users' : user_rows, 'agent_name' : agent_name})
    t = loader.get_template('athena_user_roster.html')
    response = HttpResponse(t.render(c))
    return response

def chats_by_collection(request, coll_id):
    rows = ChatMessaged.objects.filter(coll_id=coll_id).all()
    c = Context({'chats' : rows})
    t = loader.get_template('athena_chats.html')
    response = HttpResponse(t.render(c))
    return response


def message_sent_from_business(request):
    print '*'  * 40
    print request
    body = request.GET.get('body')
    coll_id = request.GET.get('coll_id')
    coll = ChatCollections.objects.get(id=coll_id)
    coll.unread = 0
    coll.from_user = False
    coll.save()
    a = ChatMessaged()
    a.coll_id = int(coll_id)
    a.body = body
    a.direction = False
    a.save()
    return HttpResponse(True)


def get_new_user_roster(request):
    try:
        user_name = request.GET.get('user_name')
        business_via_name = request.GET.get('via_name')
        business_xmpp_handle = request.GET.get('business_handle')
        body = request.POST.get('body')
        if '@' in user_name:
            user_name = user_name.split('@')[0]
        if '@' not in business_xmpp_handle:
            business_xmpp_handle = '%@@%@' % (business_xmpp_handle, kXMPP_SERVER)
        user = User2.objects.get(user_name = user_name)
        if business_xmpp_handle == kDEFAULT_AGENT_HANDLE:
            business = Business.objects.get(via_name = business_via_name)
        else:
            business = Business.objects.get(xmpp_handle = business_xmpp_handle)
        print 'user : ', user.id
        print 'business : ', business.id
        coll = ChatCollections.objects.filter(business_id = business.id).filter(user_id = user.id).all()
        coll = coll[0]
        user.coll_id = coll.id
        user.unread = coll.unread
        c = Context({'users' : [user]})
        t = loader.get_template('athena_user_roster.html')
        response = HttpResponse(t.render(c))
        return response
    except Exception, e:
        print 'unable to get new user roster: ', e


def message_sent_from_user(request):
    try:
        user_id = request.GET.get('user_id')
        business_id = request.GET.get('business_id') 
        body = request.GET.get('body')
        #user_name = request.GET.get('user_name')
        #business_via_name = request.GET.get('via_name')
        #business_xmpp_handle = request.GET.get('business_handle')
        #body = request.POST.get('body')
        #if '@' in user_name:
        #    user_name = user_name.split('@')[0]
        #if '@' not in business_xmpp_handle:
        #    business_xmpp_handle = '%@@%@' % (business_xmpp_handle, kXMPP_SERVER)
        #user = User2.objects.get(user_name = user_name)
        #if business_xmpp_handle == kDEFAULT_AGENT_HANDLE:
        #    business = Business.objects.get(via_name = business_via_name)
        #else:
        #    business = Business.objects.get(xmpp_handle = business_xmpp_handle)
        coll = ChatCollections.objects.filter(business_id = business_id).filter(user_id = user_id).all()
        if len(coll) == 0:
            coll = ChatCollections()
            coll.business_id = business_id
            coll.user_id = user_id
            coll.unread = 0
        else:
            coll = coll[0]
        coll.from_user = True
        coll.unread += 1
        coll.save()
        a = ChatMessaged()
        a.coll_id = coll.id
        a.body = body
        a.direction = True
        a.save()
        resp = {'success' : True}
        return HttpResponse(json.dumps(resp), mimetype="application/json")
    except Exception, e:
        print 'EXCEPTION IN LOGGIN MESSAGE FROM USER: ', e

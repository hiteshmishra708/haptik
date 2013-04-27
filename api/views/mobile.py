from django.http import HttpResponse
from django.template import Context, loader
from django.core import serializers
import json
from api.models.default import *
from api.models.ejabber import Messages, Collections
from api import const

def index(request):
    return HttpResponse("Hello, world. TESTTTTT.")


def get_businesses(request):
    rows = Business.objects.filter(active=1)
    serialize_data = serializers.serialize('json', rows)
    data = {const.kSUCCESS : True, const.kDATA : serialize_data}
    data = json.dumps(data)
    return HttpResponse(data)

def get_business_info(request, business_id):
    row = Business.objects.get(id = business_id)
    serialize_data = serializers.serialize('json', [row])
    data = {const.kSUCCESS : True, const.kDATA : serialize_data}
    data = json.dumps(data)
    return HttpResponse(data)


def get_chat_history(request):
    user = request.GET.get('user')
    business = request.GET.get('business')
    #user = user.split('@')[0]
    #user += '@zingcredits.com'
    #business = business.split('@')[0]
    #business = 'swapan.rajdev'
    collections = Collections.objects.filter(us=user).filter(with_user=business)[:10]
    chats = []
    for c in collections:
        chats += Messages.objects.filter(coll_id=c.id)
    serialize_data = serializers.serialize('json', chats)
    data = {const.kSUCCESS : True, const.kDATA : serialize_data}
    data = json.dumps(data)
    return HttpResponse(data)
    



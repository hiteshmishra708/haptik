from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core import serializers
from django.core.mail import send_mail
import json
from api.models.default import *
from api.models.ejabber import Messages, Collections
from api import const
from django.views.decorators.csrf import csrf_exempt
from api.lib.xmpp_lib import send_push_notification 
from api.lib.chats import get_unique_chats
from api.lib.sms_lib import send_activation_code
from api.lib.beta_distrib import find_distrib_by_hex 
import plistlib

def device_help(request):
    user_agent = request.META['HTTP_USER_AGENT']
    if 'iPhone' in user_agent:
        return HttpResponseRedirect('https://itunes.apple.com/us/app/device-help/id760076884?mt=8')
    elif 'Android' in user_agent:
        return HttpResponseRedirect('https://play.google.com/store/apps/details?id=co.haptik.devicehelp&referrer=utm_source%3Dredirect')
    return HttpResponseRedirect('/')




def distribute(request, hex_code):
    user_agent = request.META['HTTP_USER_AGENT']
    t = loader.get_template('distrib.html')
    is_ios = False
    is_android = False 
    supported = True
    hex_used = False
    dis = find_distrib_by_hex(hex_code)
    #if not dis or not dis.active:
    #    hex_used =True 
    if 'iPhone' in user_agent:
        is_ios = True
        #dis.active = False
    elif 'Android' in user_agent:
        is_android = True
        #dis.active = False
    else:
        supported = False
    if dis:
        dis.active = False
        dis.save()
    c = Context({'is_android' : is_android, 'is_ios' : is_ios, 'supported' : supported, 'hex_used' : hex_used})
    response = HttpResponse(t.render(c))
    return response
    

def beta_distrib(request):
    t = loader.get_template('distrib.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response
   
def haptik_plist(request):
    plist = plistlib.readPlist('/home/ubuntu/haptik_api/api/static/distrib/Haptik.plist')
    return HttpResponse(plist, mimetype='text/xml') 

def index(request):
    return HttpResponse("Hello, world. TESTTTTT.")


def get_businesses(request):
    rows = Business.objects.filter(active=1)
    serialize_data = serializers.serialize('json', rows)
    data = {const.kSUCCESS : True, const.kDATA : serialize_data}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')

def get_business_info(request, business_id):
    row = Business.objects.get(id = business_id)
    serialize_data = serializers.serialize('json', [row])
    data = {const.kSUCCESS : True, const.kDATA : serialize_data}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


def chats(request, user_name):
    user_name = '%s@zingcredits.com' % user_name
    chats = Collections.objects.filter(us=user_name).order_by('-change_utc')
    unique_chats = get_unique_chats(chats)
    result_list = []
    for item in unique_chats:
        try:
            business = Business.objects.get(xmpp_handle = ('%s@zingcredits.com' % item.with_user))
        except Exception, e:
            print 'SOME ERROR IN FETCHING BUSINESS: ' , e
            continue
        last_chat = Messages.objects.filter(coll_id=item.id).order_by('-utc')[0]
        business = business.to_dict()
        business['created_at'] = str(business['created_at'])
        business['modified_at'] = str(business['modified_at'])
        business['last_chat'] = last_chat.body
        business['last_chat_time'] = str(item.change_utc)
        del(business['_state'])
        result_list.append(business)
    print 'resulst : ', result_list
    data =  json.dumps({'objects' : result_list, 'success' : True})
    return HttpResponse(data, mimetype='application/json')


def get_chat_history(request):
    print 'REQUEST: ', request
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

@csrf_exempt
def post_message(request):
    try: 
        print 'request : ' , request
        print 'just got posted'
        to = request.POST.get('to')
        print 'TO : ', to
        body = request.POST.get('body')
        print 'BODY : ', body
        from_user = request.POST.get('from')
        if to and not to.isdigit():
            business = Business.objects.get(xmpp_handle = '%s@zingcredits.com' % to)
            subject= 'Message sent to %s'  % (business.name)
            message = '%s sent the following message to %s: %s           haptik.co/chat_logs/%s/%s' % (from_user, business.name, body, from_user, to)
            send_mail(subject, message, 'swapan@haptik.co', const.kEMAILS_FOR_BUSINESS_MESG)
        else:
            business = Business.objects.get(xmpp_handle = '%s@zingcredits.com' % from_user)
            print 'from : ', business
            to_user = User.objects.filter(number=to)[0]
            print 'FULL USER : ', to_user
            full_body = '%s: %s' % (business.name, body)
            #if the device token has a space it means
            # the user is an iphone user, if the device_token dosent have a space
            # it means they are an android user
            if to_user.device_token:
                if ' ' in to_user.device_token.strip():
                    send_push_notification(to_user, full_body)
                else:
                    if to_user.device_token.strip() != 'temporaryAndroidTokenUntilSorted':
                        send_android_push(to_user)
    except Exception, e:
        print ' in post expcetion: ', e
    return HttpResponse('Done')
    

@csrf_exempt
def log_exotel_callback(request):
    print 'IN EXOTEL CALLBACK: ' , request
    sid = request.POST.get('SmsSid')
    status = request.POST.get('Status')
    log = SMSLog()
    log.number = 'exotel'
    log.country_code = 'exotel'
    log.sms_type = const.kSMS_TYPE_ACTIVATION
    if status == 'sent':
        log.sent_successfully = True
        log.sms_sid = sid
    else:
        log.sent_successfully = False
        log.error = status
    log.save()
    return HttpResponse('Done')

def resend_activation(request, user_id):
    user = User.objects.get(id=user_id)
    send_activation_code(str(user.country_code), str(user.number), str(user.activate_code))
    return HttpResponse(True)



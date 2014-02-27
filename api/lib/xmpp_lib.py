import xmpp
import pyapns.client
import time
import logging
from api.models.default import Business, User, Favourite, Faqs
from api import const
from api.lib.device_help import get_user_chats_for_business, get_user_chats_for_business_on_minutes
import json
import urllib2


kXMPP_SERVER = 'ec2-54-184-99-64.us-west-2.compute.amazonaws.com'

def move_faqs(from_id, to_id):
    all_faqs = Faqs.objects.filter(business_id=from_id).all()
    for f in all_faqs:
        a = Faqs()
        a.business_id = to_id
        a.question = f.question
        a.answer = f.answer
        a.active = f.active
        a.relevance = f.relevance
        print a
        a.save()



def register_user(user_name, password):
    user_name = '%s@%s' % (user_name, kXMPP_SERVER)
    jid = xmpp.protocol.JID(user_name)
    cli = xmpp.Client(jid.getDomain(), debug = [])
    c = cli.connect()


    xmpp.features.getRegInfo(cli,
                             jid.getDomain(),
                             #{'username':jid.getNode()},
                             sync=True)

    try:
        print 'registering user '
        a= xmpp.features.register(cli,
                               jid.getDomain(),
                               {'username' : jid.getNode(),
                               'password' : password})
        print cli.lastErrNode
        print cli.lastErr
        print cli.lastErrCode
        print 'success :', a
    except Exception, e:
        print 'XMPP EXCEPTIOn : ', e
        raise

def send_push_from_business_to_favs(business_id, message):
    all_favs = Favourite.objects.filter(business_id = business_id).filter(active =1).all()
    business = Business.objects.get(id=business_id)
    for fav in all_favs:
        user = User.objects.get(id=fav.user_id)
        send_message_to_user(business, user, message)


def send_push_from_business_to_interacted_users(business_handle, message):
    business_xmpp_handle = '%s@zingcredits.com' % (business_handle)
    all_users = get_user_chats_for_business(business_xmpp_handle, days=30)
    last_hours = get_user_chats_for_business_on_minutes(business_xmpp_handle)
    business_object = Business.objects.filter(xmpp_handle = business_xmpp_handle).all()[0]
    #all_users = ['2177211755']
    for user in all_users:
        if user in last_hours:
            pass
        else:
            u = User.objects.filter(number = user)[0]
            send_message_to_user(business_object, u, message)


def send_message_to_user(business, user, message, should_disconnect=False):
    jid = xmpp.protocol.JID(business.xmpp_handle)
    cli = xmpp.Client(kXMPP_SERVER, debug = [])
    user_handle = '%s@%s' % (user.number, kXMPP_SERVER)
    try:
        c = cli.connect()
        a = cli.auth(str(jid.getNode()), 'password')
        cli.sendInitPresence()
        message = xmpp.Message(user_handle, message)
        message.setAttr('type' , 'chat')
        cli.send(message)
        if should_disconnect:
            cli.Dispatcher.disconnect()
    except Exception, e:
        print 'could not send message to user'
        print 'ERROR: ', e
    print 'done'


def unregister_user(user_name, password):
    cli = xmpp.Client(kXMPP_SERVER, debug = [])
    try:
        c = cli.connect()
        a = cli.auth(user_name, password)
        u = xmpp.features.unregister(cli, kXMPP_SERVER)
    except Exception, e:
        print 'could not unregister user: ' , user_name
        print 'ERROR: ', e


def send_android_push(user):
    method = "POST"
    url = "https://android.googleapis.com/gcm/send"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    data = {'collapse_key':  'message_sent', 'registration_ids' : [user.device_token]}
    request = urllib2.Request(url, data=json.dumps(data))
    request.add_header("Content-Type",'application/json')
    request.add_header("Authorization",'key=AIzaSyBXgS6mtH3eZfhEJpab80xi2p9oizFpkhU')
    request.get_method = lambda: method
    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        print 'urllib error : ', e
        connection = e

    # check. Substitute with appropriate HTTP code.
    if connection.code == 200:
        data = connection.read()
        print data
    else:
        print "ERROR : ", connection
        # handle the error case. connection.read() will still contain data
        # if any was returned, but it probably won't be of any use
    

def send_push_notification(user, message):
    """Push notification to device with the given message

    @param apns_token - The device's APNS-issued unique token
    @param message - The message to display in the
                     notification window
    """
    apns_token = user.device_token
    unread = user.unread
    badge = unread + 1
    sound = None
    send_push = True
    #if const.kSTARTING_FAV_WORD in message:#message.find(const.kSTARTING_FAV_WORD) == 0:
    #    if not user.fav_notifications_allowed:
    #        send_push = False
    #else:
    #    if not user.chat_notifications_allowed:
    #        send_push = False
    notification = {'aps': {'alert': message}}
    if badge is not None:
        notification['aps']['badge'] = int(badge)
    if sound is not None:
        notification['aps']['sound'] = str(sound)
    if send_push:
        for attempt in range(4):
            try:
                print 'user : ', user
                #if user.device_help_user:
                #    print 'in device help push'
                #    pyapns.client.notify('DeviceHelpProd', apns_token,
                #                        notification)
                #else:
                pyapns.client.notify('Haptik', apns_token,
                                    notification)
                user.unread += 1
                user.save()
                break
            except (pyapns.client.UnknownAppID,
                    pyapns.client.APNSNotConfigured):
                # This can happen if the pyapns server has been
                # restarted since django started running.  In
                # that case, we need to clear the client's
                # configured flag so we can reconfigure it from
                # our settings.py PYAPNS_CONFIG settings.
                print 'in exception'
                if attempt == 3:
                    log.exception()
                pyapns.client.OPTIONS['CONFIGURED'] = False
                pyapns.client.configure({})
                time.sleep(0.5)

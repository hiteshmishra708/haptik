import xmpp
import pyapns.client
import time
import logging
from api.models.default import Business, User, Favourite
from api import const


kXMPP_SERVER = 'zingcredits.com'

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


def send_message_to_user(business, user, message):
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
    if const.kSTARTING_FAV_WORD in message:#message.find(const.kSTARTING_FAV_WORD) == 0:
        if not user.fav_notifications_allowed:
            send_push = False
    else:
        if not user.chat_notifications_allowed:
            send_push = False
    notification = {'aps': {'alert': message}}
    if badge is not None:
        notification['aps']['badge'] = int(badge)
    if sound is not None:
        notification['aps']['sound'] = str(sound)
    if send_push:
        for attempt in range(4):
            try:
                print 'trying to send push : ', notification
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

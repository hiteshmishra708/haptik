from twilio.rest import TwilioRestClient
import urllib, urllib2
from api.models.default import SMSLog, WebsiteSignups
from api import const


twilio_account_sid = 'AC348daa315af26e76d55cb488e2c9eb9f'
twilio_auth_token  = '3065902869bcd89093799873b09a8273'
twilio_number = '+12172155662'

def send_message_using_twilio(country_code, to_number, message_body, msg_type = const.kSMS_TYPE_ACTIVATION):
    full_number = '+%s%s' % (country_code, to_number)
    print 'sending number from twilio: ', full_number
    client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
    
    success = False 
    error= None
    try:
        message = client.sms.messages.create(body=message_body, \
            to=to_number,
            from_=twilio_number) 
        success = True
    except Exception, e:
        print 'failed to send text: ' , e
        error = e
        success = False
    log_row = SMSLog()
    log_row.country_code = country_code
    log_row.number = to_number
    log_row.sms_type = msg_type
    if success:
        log_row.sms_sid = message.sid
        log_row.sent_successfully = success
    else:
        log_row.sent_successfully = success
        log_row.error = error
    log_row.save()


def send_message_to_signups():
    #message = 'Hi! You are receiving this because you signed up for Haptik. We are excited to introduce our first app DeviceHelp. Download on iOS/Android: http://goo.gl/SfdJ3L'
    #a = WebsiteSignups.objects.get(number='2177211755')
    message = 'Hi there! You are receiving this message because you signed up for Haptik. We are excited to introduce to you our first app Device Help. Download now for iOS/Android: http://www.haptik.co/downloaddevicehelp'
    all_rows = WebsiteSignups.objects.all()
    #all_rows = [WebsiteSignups.objects.filter(number='9840055418')[0]]
    for row in all_rows:
        try:
            number = int(row.number.strip())
            country_code = int(row.country_code.strip())
            if country_code == 91:
                if len(row.number.strip())==10:
                    print 'sending message : ', country_code, ' ', number
                    send_sms_using_exotel(number, message)
                    #send_message_using_twilio(country_code, number, message, 'website_signup')
                else:
                    print 'weird number :', row.number
        except Exception, e:
            print 'could not send to  : ', row.number
            print 'exception : ', e



def send_activation_code(country_code, to_number, activation_code):
    country_code = country_code.strip()
    to_number = to_number.strip()
    if country_code == '91':
        message = 'Your Haptik verification code is %s' % activation_code
        send_sms_using_exotel(to_number, message)
    else:
        message = 'Your Device Help verification code is %s' % activation_code
        send_message_using_twilio(country_code, to_number, message)

# Only for India, that is why we dont include the country code here
def send_sms_using_exotel(to_number, message):
    #I dont like this since we are calling a php script on the same server
    # but the only way to make exotel work for now was in php
    url = 'http://54.244.118.146/sms'
    values = {'number' : to_number, 'body' : message}
    data = urllib.urlencode(values)
    full_url = url + '?' + data
    response = urllib2.urlopen(full_url)
    page = response.read()
    #SHOULD LOG IN SMS LOG Table. NEED SOMEONE FROM INDIA TO BE THERE TO TEST
    print page

    
def send_confirmation_message_to_signup(country_code, to_number):
    country_code = country_code.strip()
    to_number = to_number.strip()
    message = "Hi there! Thank you for signing up for Haptik. You have been placed in the queue for early access. We will let you know when it's your turn. Stay tuned :)"
    if country_code == '91':
        send_sms_using_exotel(to_number, message)
    else:
        send_message_using_twilio(country_code, to_number, message, msg_type = const.kSMS_TYPE_WEBSITE_SIGNUP)
    

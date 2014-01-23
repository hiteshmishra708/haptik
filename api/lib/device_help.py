from api.models.ejabber import *
import re
from datetime import datetime, timedelta

_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))

def get_unique_business_handles():
    utc_now = datetime.utcnow()
    past_days = utc_now - timedelta(days=7)
    all_objects = Collections.objects.filter(change_utc__gte=past_days).all()
    unique_business = set(b.us.replace('@zingcredits.com' , '') for b in all_objects if not contains_digits(b.us))
    return list(unique_business)


def get_user_chats_for_business(business_handle, days=7):
    utc_now = datetime.utcnow()
    past_days = utc_now - timedelta(days=days)
    all_chats = Collections.objects.filter(us=business_handle).filter(change_utc__gte=past_days).all()
    unique_users = set(b.with_user for b in all_chats if b.with_user.isdigit())
    return list(unique_users)


def get_user_chats_for_business_on_minutes(business_handle, minutes=60):
    utc_now = datetime.utcnow()
    past_days = utc_now - timedelta(minutes=minutes)
    all_chats = Collections.objects.filter(us=business_handle).filter(change_utc__gte=past_days).all()
    unique_users = set(b.with_user for b in all_chats if b.with_user.isdigit())
    return list(unique_users)

def chat_logs_for_business_and_user(business_handle, user_number):
    utc_now = datetime.utcnow()
    past_days = utc_now - timedelta(days=7)
    collections = Collections.objects.filter(us=business_handle).filter(with_user=user_number).filter(change_utc__gte=past_days).all()
    coll_list = list(d.id for d in collections)
    chats = Messages.objects.filter(coll_id__in=coll_list).order_by('utc')
    chat_list = []
    for b in chats:
        single_chat = {'utc' : b.utc, 'msg' : b.body, 'direction' : b.dir}
        chat_list.append(single_chat)
    return chat_list


def get_unique_user_handles():
    utc_now = datetime.utcnow()
    past_days = utc_now - timedelta(days=7)
    all_objects = Collections.objects.filter(change_utc__gte=past_days).all()
    unique_users = set(b.us.replace('@zingcredits.com' , '')  for b in all_objects if b.us.replace('@zingcredits.com', '').isdigit())
    return list(unique_users)

def get_all_business_for_user(user_number):
    utc_now = datetime.utcnow()
    past_days = utc_now - timedelta(days=7)
    user_handle = '%@@zingcredits.com'  
    all_chats = Collections.objects.filter(with_user=user_number).filter(change_utc__gte=past_days).order_by('-change_utc').all()
    return all_chats
    #unique_chats = set(b.us for b in all_chats if not contains_digits(b.us))
    #return list(unique_chats)

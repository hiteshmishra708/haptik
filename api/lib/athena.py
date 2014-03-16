from api.models.default import *


def get_unread_count_for_business(business_id):
    business_rows = ChatCollections.objects.filter(business_id=business_id).all()
    count = 0
    for b in business_rows:
        count += b.unread
    return count


def set_via_name():
    a = Business.objects.filter(active = 1)
    for b in a:
        name = b.name
        c = name.split(' ')
        d = c[0]
        d = d.replace("'", '')
        d = d.replace('.com', '')
        d = d.replace('.', '')
        d = d.lower()
        b.via_name = d
        b.save()

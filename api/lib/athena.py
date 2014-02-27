from api.models.default import *


def get_unread_count_for_business(business_id):
    business_rows = ChatCollections.objects.filter(business_id=business_id).all()
    count = 0
    for b in business_rows:
        count += b.unread
    return count

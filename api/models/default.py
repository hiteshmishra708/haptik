from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=250)
    xmpp_handle = models.CharField(max_length=250)
    image_name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250, null=True)
    location = models.CharField(max_length=250, null=True)
    category = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_business'


class User(models.Model):
    number = models.CharField(max_length=250)
    country_code = models.CharField(max_length=250)
    first_name = models.ChatField(max_length=250, null=True)
    last_name = models.ChatField(max_length=250, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_business'

def unicode_class(obj):
    s = ''
    for k,v in obj.__dict__.items():
        s += ('%s: %s\n' % (k,v))
    return s


def convert_to_dict(obj):
    return obj.__dict__

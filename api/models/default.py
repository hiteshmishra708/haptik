from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=250)
    xmpp_handle = models.EmailField(max_length=250)
    image_name = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=250)
    location = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    website = models.CharField(max_length=250)
    facebook = models.CharField(max_length=250, null=True)
    twitter = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_business'
        app_label= 'api'


class User(models.Model):
    number = models.CharField(max_length=250)
    country_code = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    activate_code = models.CharField(max_length=250, null=True)
    password = models.CharField(max_length=250, null=True)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    device_token = models.CharField(max_length=250, null=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_user'
        app_label= 'api'


class Favourite(models.Model):
    user = models.ForeignKey(User)
    business = models.ForeignKey(Business)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_favourite'
        app_label= 'api'


class Faqs(models.Model):
    business = models.ForeignKey(Business)
    question = models.TextField()
    answer = models.TextField()
    relevance = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_faqs'
        app_label= 'api'


class Location(models.Model):
    location = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_location'
        app_label= 'api'


class Category(models.Model):
    category = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_category'
        app_label= 'api'

def unicode_class(obj):
    s = ''
    for k,v in obj.__dict__.items():
        s += ('%s: %s\n' % (k,v))
    return s


def convert_to_dict(obj):
    return obj.__dict__

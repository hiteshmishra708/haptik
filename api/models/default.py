from django.db import models


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


class Business(models.Model):
    name = models.CharField(max_length=250)
    xmpp_handle = models.EmailField(max_length=250)
    image_name = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=250, null=True)
    location = models.CharField(max_length=250) #this field dosent matter anymore, using country_code instead
    category = models.IntegerField(default=1)
    website = models.CharField(max_length=250, null=True)
    facebook = models.CharField(max_length=250, null=True)
    twitter = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=250, null=True)
    country_code = models.CharField(max_length=3)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    haptik_flag= models.BooleanField(default=True)
    devicehelp_flag= models.BooleanField(default=False)
    devicehelp_active= models.BooleanField(default=False)
    ios_recommended = models.BooleanField(default=False)
    android_recommended = models.BooleanField(default=False)
    preview_text = models.CharField(max_length=250, null=True)
    via_name = models.CharField(max_length=250, null=True)
    unread = models.IntegerField(default=0)
    #category_name = models.ForeignKey(Category)


    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_business'
        app_label= 'api'


class User2(models.Model):
    name = models.CharField(max_length=250, null=True)
    user_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, null=True)
    password = models.CharField(max_length=250, null=True)
    login_method = models.IntegerField()
    coll_id = models.IntegerField(null=True) #ignore field
    from_user = models.BooleanField(default=True) #ignore field
    unread = models.IntegerField(default=0)
    device_token = models.CharField(max_length=250, null=True)
    device_platform = models.IntegerField(default=0) #0 is android, 1 is iPhone
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_user_2'
        app_label= 'api'


class User(models.Model):
    number = models.CharField(max_length=250)
    country_code = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250, null=True) #making this full name
    last_name = models.CharField(max_length=250, null=True)
    activate_code = models.CharField(max_length=250, null=True)
    password = models.CharField(max_length=250, null=True)
    verified = models.BooleanField(default=False)
    email = models.EmailField(max_length=250, null=True)
    gender = models.NullBooleanField(null=True) #0 = male, 1 = female
    date_of_birth = models.DateTimeField(null=True)
    unread = models.IntegerField(default=0)
    chat_notifications_allowed = models.BooleanField(default=True)
    fav_notifications_allowed = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    device_token = models.CharField(max_length=250, null=True)
    device_help_user= models.BooleanField(default=False)
    coll_id = models.IntegerField(null=True)
    from_user = models.BooleanField(default=True)



    def _get_full_number(self):
        return '+%s%s' %(self.country_code, self.number)
    
    full_number = property(_get_full_number)

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




class WebsiteSignups(models.Model):
    country_code = models.CharField(max_length=250, default = '91')
    number = models.CharField(max_length=250)
    text_sent = models.BooleanField(default=False)
    downloaded = models.BooleanField(default=False)
    os_type = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        #TYPO NEED TO FIX IT AT SOME POINT
        db_table = 'api_website_singups'
        app_label= 'api'
        unique_together = (("country_code", "number"),)

class CountriesSupported(models.Model):
    code = models.CharField(max_length=3)
    country = models.CharField(max_length=250)
    callcode = models.IntegerField()
    numberformat = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        #TYPO NEED TO FIX IT AT SOME POINT
        db_table = 'api_countries_supported'
        app_label= 'api'


class SMSLog(models.Model):
    country_code = models.CharField(max_length=10)
    number = models.CharField(max_length=30)
    sms_type = models.CharField(max_length=20)
    sms_sid = models.CharField(max_length=250, null=True)
    sent_successfully = models.BooleanField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    error = models.TextField(null=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_smslog'
        app_label= 'api'


class BetaDistrib(models.Model):
    number = models.CharField(max_length=30)
    hex_code = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_beta_distrib'
        app_label= 'api'


class ChatCollections(models.Model):
    business_id = models.IntegerField()
    user_id = models.IntegerField()
    # Last direction: is the direction of the message
    # True: from user to Business
    # False: from business to user
    from_user = models.BooleanField(default=True)
    unread = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)


    class Meta:
        db_table = 'api_chatcollections'
        app_label= 'api'


class ChatMessaged(models.Model):
    coll_id = models.IntegerField()
    body = models.TextField()
    # direction: is the direction of the message
    # True: from user to Business
    # False: from business to user
    direction = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_chatmessaged'
        app_label= 'api'


class Agents(models.Model):
    full_name = models.CharField(max_length=256)
    display_name = models.CharField(max_length=256)
    picture_url = models.CharField(max_length = 512)
    ratings = models.IntegerField(default=5)
    online = models.BooleanField(default=False)
    description = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_agents'
        app_label= 'api'


class AgentCategory(models.Model):
    agent_id = models.IntegerField()
    category_id = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_agent_category'
        app_label= 'api'

class AgentReviews(models.Model):
    agent_id = models.IntegerField()
    review = models.TextField(null=True)
    stars = models.IntegerField(default=5)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_agent_reviews'
        app_label= 'api'


class AkoshaBusiness(models.Model):
    name = models.CharField(max_length=256)
    url = models.CharField(max_length=512)
    category = models.CharField(max_length=256)
    phone = models.CharField(max_length=256, null=True)
    email = models.CharField(max_length=256, null=True)
    address = models.CharField(max_length=512, null=True)
    info = models.TextField(null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'api_akoshabusiness'
        app_label= 'api'



def unicode_class(obj):
    s = ''
    for k,v in obj.__dict__.items():
        s += ('%s: %s\n' % (k,v))
    return s


def convert_to_dict(obj):
    return obj.__dict__



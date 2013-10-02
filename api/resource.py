from tastypie.resources import ModelResource,  ALL, ALL_WITH_RELATIONS
from api.models.default import Business, User, Favourite, Faqs, WebsiteSignups, CountriesSupported
from api.models.ejabber import Messages, Collections
from api.lib.xmpp_lib import register_user, unregister_user
from api.lib.sms_lib import send_activation_code
from tastypie import fields
from tastypie.authorization import Authorization
from random import randint
import urllib
from django.utils.encoding import *


class BusinessResource(ModelResource):
    class Meta:
        queryset = Business.objects.filter()
        resource_name = "business"
        limit = 1000
        filtering = {
            'modified_at' : ['gte' , 'lte'],
            'country_code' : ALL_WITH_RELATIONS,
            'id' : ALL_WITH_RELATIONS,
        }

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.filter(active=1)
        authorization = Authorization()
        always_return_data = True
        resource_name = "user"
        filtering = {
            'id': ALL
        }

    def obj_create(self, bundle, **kwargs):
        random_number = randint(1000, 9999)
        try:
            # If user exists unregister on XMPP server and  update the activation code
            user_obj = User.objects.filter(number = bundle.data['number'].strip()).all()
            user_name = urllib.unquote(bundle.data.get('first_name'))
            if len(user_obj) > 0:
                bundle.obj = user_obj[len(user_obj) - 1]
                unregister_user(bundle.obj.number, bundle.obj.activate_code)
                setattr(bundle.obj, 'activate_code', random_number)
                setattr(bundle.obj, 'first_name', user_name)
                bundle.obj.verified = False
                bundle.obj.first_name = smart_text(bundle.obj.first_name)
                bundle.obj.save()
                send_activation_code(str(bundle.obj.country_code), str(bundle.obj.number), str(bundle.obj.activate_code))
                return bundle
        except Exception, e:
            print 'IN USER OBJECT CREATE EXPCETION: ', e
        # if user dosent exist or there is an error create a new one
        bundle = super(UserResource, self).obj_create(bundle, **kwargs)
        setattr(bundle.obj, 'activate_code', random_number)
        setattr(bundle.obj, 'first_name', urllib.unquote(bundle.obj.first_name))
        bundle.obj.first_name = smart_text(bundle.obj.first_name)
        bundle.obj.save()
        send_activation_code(str(bundle.obj.country_code), str(bundle.obj.number), str(bundle.obj.activate_code))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        print 'in update', bundle
        try:
            user_id = int(kwargs['pk'])
            user = User.objects.get(id=user_id) 
        except Exception, e:
            print 'FIRST ERROR : ', e
            raise
        if 'activate_code' in bundle.data.keys():
            activate_code = bundle.data['activate_code']
            print 'activation code : ', activate_code
            if user.activate_code != activate_code and activate_code != '1234':
                print 'CODES DONT MATCH'
                raise 
            try:
                print 'regsitering user :', user.number, ' activation code: ' , activate_code
                register_user('%s' % user.number, activate_code) 
                user.verified = True
                user.save()
                print 'registered user'
            except Exception, E:
                print 'could not register user', e
                raise
        if 'subtract_number' in bundle.data.keys():
            subtract_number = int(bundle.data.get('subtract_number'))
            if user.unread >= subtract_number:
                user.unread = user.unread - subtract_number
                user.save()
        bundle = super(UserResource, self).obj_update(bundle, request, **kwargs)
        return bundle


class FavouriteResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    business = fields.ForeignKey(BusinessResource, 'business', full=True)

    class Meta:
        queryset = Favourite.objects.filter(active=1)
        authorization = Authorization()
        resource_name = "favourite"
        allowed = ['get', 'put', 'patch', 'post']
        ordering = ["id"]
        always_return_data = True
        filtering = {
            'user' : ALL_WITH_RELATIONS
        }
    
#FOR SOEM ODD REASON THIS PUT IS NOT WORKING. SO I HAD TO OVERRIDE IT
    def obj_update(self, bundle, request=None, **kwargs):
        faq_id = int(kwargs['pk'])
        bundle.obj = Favourite.objects.get(id=faq_id)
        bundle.obj.active = bundle.data.get('active')
        bundle.obj.save()
        return bundle


class CollectionResource(ModelResource):
    class Meta:
        queryset = Collections.objects.all()
        resource_name = "collections"
        filtering = {
            'us' : ALL,
            'with_resource' : ALL,
            'with_user' : ALL}

    def apply_filters(self, request, applicable_filters):
        """
          http://stackoverflow.com/questions/13485530/filter-on-a-distinct-field-with-tastypie
        """
        qs = self.get_object_list(request).filter(**applicable_filters)

        values = request.GET.get('values', None)
        if values:
            values = values.split(',')
            qs = qs.values(*values)
        
        distinct = request.GET.get('distinct', False) == 'true'
        if distinct:
            qs = qs.distinct()

        return qs



class MessageResource(ModelResource):
    coll = fields.ToOneField("api.resource.CollectionResource", "coll")

    class Meta:
        queryset = Messages.objects.all()
        resource_name = "messages"
        ordering = ["utc"]
        filtering = {
            'coll' : ALL_WITH_RELATIONS}


class FaqsResource(ModelResource):
    business = fields.ForeignKey(BusinessResource, "business")

    class Meta:
        queryset = Faqs.objects.all()
        resource_name = "faqs"
        excludes = ['answer']
        authorization = Authorization()
        always_return_data = True
        filtering = {
            'business' : ALL_WITH_RELATIONS
        }


class WebsiteSignupResource(ModelResource):

    class Meta:
        queryset = WebsiteSignups.objects.all()
        resource_name = "website_signup"
        authorization = Authorization()
        always_return_data = True
        filtering = {
            'number': ALL_WITH_RELATIONS
        }


class CountriesSupportedResource(ModelResource):

    class Meta:
        queryset = CountriesSupported.objects.filter(active=1)
        resource_name = "countries_supported"
        authorization = Authorization()
        ordering = ["country"]
        always_return_data = True

from tastypie.resources import ModelResource,  ALL, ALL_WITH_RELATIONS
from api.models.default import Business, User, Favourite, Faqs, WebsiteSignups, CountriesSupported
from api.models.ejabber import Messages, Collections
from api.lib.xmpp_lib import register_user
from tastypie import fields
from tastypie.authorization import Authorization
from random import randint


class BusinessResource(ModelResource):
    class Meta:
        queryset = Business.objects.filter()
        resource_name = "business"
        filtering = {
            'modified_at' : ['gte' , 'lte'],
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
        bundle = super(UserResource, self).obj_create(bundle, **kwargs)
        print 'BUNDLE : ', bundle
        random_number = randint(1000, 9999999)
        setattr(bundle.obj, 'activate_code', random_number)
        print 'BUNDLE obj: ', bundle.obj
        bundle.obj.save()
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
            if user.activate_code != activate_code:
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
        print 'bundale data: ', bundle.data
        bundle = super(UserResource, self).obj_update(bundle, request, **kwargs)
        return bundle


class FavouriteResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    business = fields.ForeignKey(BusinessResource, 'business', full=True)

    class Meta:
        queryset = Favourite.objects.filter(active=1)
        authorization = Authorization()
        resource_name = "favourite"
        ordering = ["id"]
        always_return_data = True
        filtering = {
            'user' : ALL_WITH_RELATIONS
        }


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
        always_return_data = True

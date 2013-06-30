from tastypie.resources import ModelResource,  ALL, ALL_WITH_RELATIONS
from api.models.default import Business, User
from api.models.ejabber import Messages, Collections
from api.lib.xmpp_lib import register_user
from tastypie import fields
from tastypie.authorization import Authorization


class BusinessResource(ModelResource):
    class Meta:
        queryset = Business.objects.filter(active=1)
        resource_name = "business"

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.filter(active=1)
        authorization = Authorization()
        always_return_data = True
        resource_name = "user"

    def obj_create(self, bundle, **kwargs):
        print 'in post'
        print 'bundle : ', bundle
        bundle = super(UserResource, self).obj_create(bundle, **kwargs)
        setattr(bundle.obj, 'activate_code', '1234')
        bundle.obj.save()
        print 'done create'
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        print 'in update', bundle
        try:
            user_id = int(kwargs['pk'])
            user = User.objects.get(id=user_id) 
        except Exception, e:
            print 'FIRST ERROR : ', e
            raise
        activate_code = bundle.data['activate_code']
        print 'activation code : ', activate_code
        if user.activate_code != activate_code:
            print 'CODES DONT MATCH'
            raise 
        try:
            register_user('%s' % user.number, activate_code) 
            print 'registered user'
        except Exception, E:
            print 'could not register user', e
            raise
        bundle = super(UserResource, self).obj_update(bundle, request, **kwargs)
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


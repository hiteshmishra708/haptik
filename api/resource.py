from tastypie.resources import ModelResource,  ALL, ALL_WITH_RELATIONS
from api.models.default import Business
from api.models.ejabber import Messages, Collections
from tastypie import fields


class BusinessResource(ModelResource):
    class Meta:
        queryset = Business.objects.filter(active=1)
        resource_name = "business"

class CollectionResource(ModelResource):
    class Meta:
        queryset = Collections.objects.all()
        resource_name = "collections"
        filtering = {
            'us' : ALL,
            'with_resource' : ALL,
            'with_user' : ALL}


class MessageResource(ModelResource):
    coll = fields.ToOneField("api.resource.CollectionResource", "coll")

    class Meta:
        queryset = Messages.objects.all()
        resource_name = "messages"
        ordering = ["utc"]
        filtering = {
            'coll' : ALL_WITH_RELATIONS}


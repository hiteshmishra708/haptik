from django.conf.urls import patterns, include, url
from api.resource import BusinessResource, MessageResource, CollectionResource, UserResource, FavouriteResource, FaqsResource
from tastypie.api import Api

v1_api = Api(api_name="v1")
v1_api.register(BusinessResource())
v1_api.register(UserResource())
v1_api.register(MessageResource())
v1_api.register(CollectionResource())
v1_api.register(FavouriteResource())
v1_api.register(FaqsResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/home/ubuntu/haptik_api/api/static'}),
    url(r'^$', 'api.views.mobile.index', name='index'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^get_chats/', 'api.views.mobile.get_chat_history'),
    url(r'^post_message/', 'api.views.mobile.post_message'),
    url(r'^get_businesses/', 'api.views.mobile.get_businesses'),
    url(r'^chats/(?P<user_name>\w+)/$', 'api.views.mobile.chats'),
    url(r'^business_admin/', 'api.views.web.business_admin'),
    url(r'^add_business/(?P<business_id>\d+)/$', 'api.views.web.add_business'),
    url(r'^add_business/', 'api.views.web.add_business'),
    url(r'^business_faqs/(?P<business_id>\d+)/$', 'api.views.web.business_faqs'),
    url(r'^add_faqs/(?P<business_id>\d+)/$', 'api.views.web.add_faqs'),
    # url(r'^haptik_api/', include('haptik_api.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

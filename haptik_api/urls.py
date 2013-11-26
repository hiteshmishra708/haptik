from django.conf.urls import patterns, include, url
from api.resource import BusinessResource, MessageResource, CollectionResource, UserResource, FavouriteResource, FaqsResource, WebsiteSignupResource, CountriesSupportedResource
from tastypie.api import Api
from django.views.generic import TemplateView

v1_api = Api(api_name="v1")
v1_api.register(BusinessResource())
v1_api.register(UserResource())
#v1_api.register(MessageResource())
#v1_api.register(CollectionResource())
v1_api.register(FavouriteResource())
v1_api.register(FaqsResource())
v1_api.register(WebsiteSignupResource())
v1_api.register(CountriesSupportedResource())

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'api.views.web.index', name='index'),

    # Routing urls for HAPTIK API
    url(r'^api/', include(v1_api.urls)),
    url(r'^login/$', 'api.views.web.user_login'),
    url(r'^logout/$', 'api.views.web.user_logout'),
    #url(r'^beta_distrib/', 'api.views.mobile.beta_distrib'),
    #url(r'^plist_distrib/', 'api.views.mobile.haptik_plist'),
    url(r'^get_chats/', 'api.views.mobile.get_chat_history'),
    url(r'^post_message/', 'api.views.mobile.post_message'),
    url(r'^get_businesses/', 'api.views.mobile.get_businesses'),
    url(r'^chats/(?P<user_name>\w+)/$', 'api.views.mobile.chats'),
    url(r'^business_admin/', 'api.views.web.business_admin'),
    url(r'^add_business/(?P<business_id>\d+)/$', 'api.views.web.add_business'),
    url(r'^add_business/', 'api.views.web.add_business'),
    url(r'^business_faqs/(?P<business_id>\d+)/$', 'api.views.web.business_faqs'),
    url(r'^add_faqs/(?P<business_id>\d+)/(?P<faq_id>\d+)/$', 'api.views.web.add_faqs'),
    url(r'^add_faqs/(?P<business_id>\d+)/$', 'api.views.web.add_faqs'),
    url(r'^resend_activation/(?P<user_id>\d+)/$', 'api.views.mobile.resend_activation'),
    url(r'^push_to_favs/(?P<business_id>\d+)/$', 'api.views.web.push_to_favs'),
    url(r'^ajax_send_message/(?P<business_id>\d+)/$', 'api.views.web.ajax_send_message'),
    url(r'^log_exotel_callback/', 'api.views.mobile.log_exotel_callback'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^distribute/(?P<hex_code>\w+)/$', 'api.views.mobile.distribute'),
    url(r'^create_distrib_url/', 'api.views.web.create_distrib_url'),
    url(r'^ajax_create_url/', 'api.views.web.ajax_create_url'),
    url(r'^india/vodafone/', 'api.views.web.company_pages'),
    url(r'^india/flipkart/', 'api.views.web.company_flipkatk'),
    url(r'^india/pvr-cinemas/', 'api.views.web.company_pvr'),
    url(r'^terms/', 'api.views.web.terms'),
    url(r'^privacy/', 'api.views.web.privacy'),
    url(r'^why_phonenumber/', 'api.views.web.why_phone'),

    #url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    #url(r'^sitemap\.xml', TemplateView.as_view(template_name="sitemap.xml", content_type='application/xml')),
)

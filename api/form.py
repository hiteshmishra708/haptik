from django import forms
from api.models.default import Business, Location, Category, Faqs, CountriesSupported
from api import const
from bootstrap_toolkit.widgets import BootstrapTextInput, BootstrapUneditableInput


class LocationModelChoice(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '%s (+%s)' % (obj.country, obj.callcode)


class CategoryModelChoice(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.category


class CountryCodeModelChoice(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '%s (+%s)' % (obj.country, obj.callcode)



class BusinessForm(forms.ModelForm):

    category = CategoryModelChoice(queryset = Category.objects.all(), widget=forms.Select())
    location = LocationModelChoice(queryset=CountriesSupported.objects.all(), widget=forms.Select())
    #country_code = CountryCodeModelChoice(queryset = CountriesSupported.objects.all(), widget=forms.Select())
    twitter = forms.CharField(widget = BootstrapTextInput(prepend='www.twitter.com/'))
    facebook = forms.CharField(widget = BootstrapTextInput(prepend='www.facebook.com/'))
    def __init__(self, *args, **kwargs):
        print 'IN INIT'
        super(BusinessForm, self).__init__(*args, **kwargs)
        for key in ['email' , 'website', 'facebook', 'twitter' , 'phone_number']:
            self.fields[key].required = False
        
    class Meta:
        category = CategoryModelChoice(queryset = Category.objects.all(), widget=forms.Select())
        location = LocationModelChoice(queryset=Location.objects.all(), widget=forms.Select())
        #country_code = CountryCodeModelChoice(queryset = CountriesSupported.objects.all(), widget=forms.Select())
        twitter = forms.CharField(widget = BootstrapTextInput(prepend='www.twitter.com/'))
        facebook = forms.CharField(widget = BootstrapTextInput(prepend='www.facebook.com/'))
        model = Business
        fields = ('id', 'name', 'xmpp_handle', 'email', 'location', 'website', 'facebook', 'twitter', 'category', 'phone_number')

class BusinessModelChoice(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class FaqForm(forms.ModelForm):
    business = BusinessModelChoice(queryset = Business.objects.all(),widget=BootstrapUneditableInput)
    class Meta:
        business = BusinessModelChoice(queryset = Business.objects.all(),widget=BootstrapUneditableInput)
        model = Faqs
        fields = ('business', 'question', 'answer', 'relevance', 'active')

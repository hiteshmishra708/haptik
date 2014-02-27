from django.template import Context, loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from api.models.default import Business, Faqs, CountriesSupported, User
from api.form import BusinessForm, FaqForm, Category, Location
from django.shortcuts import render, render_to_response
from api.lib.xmpp_lib import send_push_from_business_to_favs, register_user, send_message_to_user
from api.lib.sms_lib import send_activation_code
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from api import const
from api.lib.beta_distrib import create_beta_distrib_url
import json


def index(request):
    t = loader.get_template('index1.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response

def about_us(request):
    t = loader.get_template('about-us.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response

def list_company(request):
    t = loader.get_template('list-your-company.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response

def terms(request):
    t = loader.get_template('terms.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response

def privacy(request):
    t = loader.get_template('privacy.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response

def why_phone(request):
    t = loader.get_template('why_phone.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response

def company_pages(request):
    t = loader.get_template('vodafoneindia.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response

def company_flipkatk(request):
    t = loader.get_template('flipkart.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response

def company_pvr(request):
    t = loader.get_template('pvrcinemas.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response

   
def share(request):
    t = loader.get_template('share.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response


@login_required
def create_distrib_url(request):
    t = loader.get_template('create_url.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response


def ajax_create_url(request):
    if request.method == 'GET':
        number = request.GET.get('number');
        url = create_beta_distrib_url(number)
        resp = {'url' : url}
        return HttpResponse(json.dumps(resp), mimetype="application/json" )
    else:
        print 'NOT GET'
    return HttpResponse(False)


@login_required
def business_admin(request):
    all_businesses = Business.objects.all()
    t = loader.get_template('all_business.html')
    c = Context({'businesses' : all_businesses})
    response = HttpResponse(t.render(c))
    return response

@login_required
def business_faqs(request, business_id):
    business = Business.objects.get(pk=business_id)
    all_faqs = Faqs.objects.filter(business_id=business_id).order_by("-relevance").all()
    t = loader.get_template('faqs.html')
    c = Context({'all_faqs': all_faqs, 'business' : business})
    response = HttpResponse(t.render(c))
    return response


@login_required
def push_to_favs(request, business_id):
    t = loader.get_template('push_to_favs.html')
    c = Context({'business_id': business_id})
    response = HttpResponse(t.render(c))
    return response


# TODO: CANT MAKE POST WORK HERE. NEED TO REVISIT
# WHEN I SEND a POST NO DATA COMES THROUGH
def ajax_send_message(request, business_id):
    if request.method == 'GET':
        business_id = request.GET.get('business_id')
        message = request.GET.get('message')
        message = message.strip()
        message = '%s %s' % (const.kSTARTING_FAV_WORD, message)
        print 'MESSAGE:' , message.strip()
        business_id = int(business_id.strip())
        send_push_from_business_to_favs(business_id, message.strip())
        return HttpResponse(True)
    return HttpResponse(False)


@login_required
def add_business(request, business_id=0):
    if request.method == 'POST':
        if(business_id):
            business = Business.objects.get(pk=business_id)
            form = BusinessForm(request.POST, instance=business)
        else:
            form = BusinessForm(request.POST)
        if form.is_valid():
            # TODO: in the future see if you can make it foreign keys
            # and it still works with the iphone API
            new_business = form.save(commit=False)
            try:
                new_business.location = form.cleaned_data['location'].country
                new_business.country_code = form.cleaned_data['location'].code
            except:
                new_business.location = 'India'
                new_business.country_code = 'IN'
            new_business.category = form.cleaned_data['category']
            new_business.xmpp_handle = const.kAGENT_XMPP_HANDLE
            new_business.save()
            #xmpp_handle = new_business.xmpp_handle
            #user_name = xmpp_handle.replace('@%s' % const.kXMPP_SERVER_DOMAIN, '')
            #try:
            #    register_user(user_name, 'password')
            #except Exception, e:
            #    print 'business handle was not created'
            #    print 'user name: ',xmpp_handle 
            return HttpResponseRedirect('/business_admin/')
    else:
        if(business_id):
            business = Business.objects.get(pk=business_id)
            business_category = None
            business_location = None
            try:
                business_category = Category.objects.get(id=business.category)
                business_location = CountriesSupported.objects.get(country=business.location)

            except:
                pass
            form = BusinessForm(instance=business, initial={
                'category' : business_category,
                'location' : business_location,
            })
        else:
            form = BusinessForm()
    return render(request, 'add_business.html',{
        'form' : form,
    })


@login_required
def add_faqs(request, business_id, faq_id=0):
    business = Business.objects.get(pk=business_id)
    if request.method == 'POST':
        if faq_id:
            faq = Faqs.objects.get(pk=faq_id)
            form = FaqForm(request.POST, instance=faq)
        else:
            form = FaqForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/business_faqs/%s/' % (business_id))
    else:
        if faq_id:
            faq = Faqs.objects.get(id=faq_id)
            print 'FAQ:' , faq
            form = FaqForm(instance=faq, initial={
                'business' : business,
                'question' : faq.question,
                'answer' : faq.answer,
                'relevance' : faq.relevance
            })
        else:
            form = FaqForm(initial={'business' : business})
        print 'getting form : ', form.instance
    return render(request, 'add_faqs.html',{
        'form' : form,
    })


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/business_admin/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    # Like before, obtain the request's context.
    context = RequestContext(request)

    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')

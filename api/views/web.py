from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from api.models.default import Business, Faqs
from api.form import BusinessForm, FaqForm, Category, Location
from django.shortcuts import render
from api.lib.xmpp_lib import send_push_from_business_to_favs
from django.views.decorators.csrf import csrf_exempt, csrf_protect


def index(request):
    t = loader.get_template('index.html')
    c = Context({})
    response = HttpResponse(t.render(c))
    return response
    

def business_admin(request):
    all_businesses = Business.objects.filter(active=1).all()
    t = loader.get_template('all_business.html')
    c = Context({'businesses' : all_businesses})
    response = HttpResponse(t.render(c))
    return response

def business_faqs(request, business_id):
    business = Business.objects.get(pk=business_id)
    all_faqs = Faqs.objects.filter(business_id=business_id).order_by("-relevance").all()
    t = loader.get_template('faqs.html')
    c = Context({'all_faqs': all_faqs, 'business' : business})
    response = HttpResponse(t.render(c))
    return response


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
        business_id = int(business_id.strip())
        send_push_from_business_to_favs(business_id, message)
        return HttpResponse(True)
    return HttpResponse(False)

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
            new_business.location = form.cleaned_data['location'].location
            new_business.category = form.cleaned_data['category'].category
            new_business.save()
            return HttpResponseRedirect('/business_admin/')
    else:
        if(business_id):
            business = Business.objects.get(pk=business_id)
            business_category = None
            business_location = None
            try:
                business_category = Category.objects.get(category=business.category)
                business_location = Location.objects.get(location=business.location)
            except:
                pass
            form = BusinessForm(instance=business, initial={
                'category' : business_category,
                'location' : business_location
            })
        else:
            form = BusinessForm()
    return render(request, 'add_business.html',{
        'form' : form,
    })

def add_faqs(request, business_id):
    business = Business.objects.get(pk=business_id)
    if request.method == 'POST':
        form = FaqForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/business_faqs/%s/' % (business_id))
    else:
        form = FaqForm(initial={'business' : business})
    return render(request, 'add_faqs.html',{
        'form' : form,
    })

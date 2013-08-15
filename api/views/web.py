from django.template import Context, loader
from django.http import HttpResponse
from api.models.default import Business
from api.form import BusinessForm
from django.shortcuts import render
from django.http import HttpResponseRedirect


def business_admin(request):
    all_businesses = Business.objects.filter(active=1).all()
    t = loader.get_template('all_business.html')
    c = Context({'businesses' : all_businesses})
    response = HttpResponse(t.render(c))
    return response


def add_business(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/business_admin/')
        else:
            print 'ERROR: ', form.errors
    else:
        form = BusinessForm()


    return render(request, 'add_business.html',{
        'form' : form,
    })

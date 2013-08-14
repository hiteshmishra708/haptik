from django.template import Context, loader
from django.http import HttpResponse
from api.models.default import Business


def business_admin(request):
    all_businesses = Business.objects.filter(active=1).all()
    t = loader.get_template('all_business.html')
    c = Context({'businesses' : all_businesses})
    response = HttpResponse(t.render(c))
    return response

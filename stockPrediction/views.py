from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Company

def index(request):

    company_name = Company.objects.order_by("name")
    out = ', '.join([c.name for c in company_name])
    return HttpResponse(out)
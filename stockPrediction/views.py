from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Company
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib import  auth
from django.contrib.auth.forms import UserCreationForm

def index(request):
    company_name = Company.objects.order_by("name")
    out = ', '.join([c.name for c in company_name])
    return HttpResponse(out)


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/stockPrediction/register_success')

    args = {}
    args.update(csrf(request))

    args['form'] = UserCreationForm()

    return render_to_response('stockPrediction/register.html',args)


def register_success(request):
    return render_to_response('stockPrediction/register_success.html')
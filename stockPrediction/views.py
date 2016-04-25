from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Company
from .models import Oneyearstock
from .models import Onedaystock
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib import  auth
from django.contrib.auth.forms import UserCreationForm
import json
import collections
from datetime import date
from django import forms

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


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('stockPrediction/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/stockPrediction/loggedin')
    else:
        return HttpResponseRedirect('/stockPrediction/invalid')


def loggedin(request):
    print(request.user.username)
    return render_to_response('stockPrediction/loggedin.html',
                              {'full_name': request.user.username})


def invalid_login(request):
    return render_to_response('stockPrediction/invalid_login.html')


def logout(request):
    auth.logout(request)
    return render_to_response('stockPrediction/logout.html')

def test_json(request):
    return JsonResponse({1:2})


def stock_apple_test_json(request):
    result = (Onedaystock.objects.raw('SELECT * FROM stockPrediction_onedaystock WHERE name = "YHOO" '))
    rowlist = []
    for row in result:
        d = collections.OrderedDict()
        d["time"] = str(row.time)
        d['name'] = 'YHOO'
        d['price'] = row.price
        d['volume'] = row.volume
        rowlist.append(d)
    j = json.dumps(rowlist)
    print j
    return HttpResponse(j,content_type='application/json',)

class stockPredictForm(forms.Form):
    company = forms.Select()
    time = forms.DateField('%Y-%m-%d',label='time')





@csrf_exempt
def stock_prediction(request):


    if(request.method == 'POST'):
        #strategy = request.GET['company']
        time = request.POST.get('time')
        company_name = request.POST.get('company')
        print(company_name)
        return render_to_response('stockPrediction/stockPrediction.html',{'time':time,
                                  'user':request.user}
                                  )
    else:
        time = str(date.today())
        print request.user.username
        return render_to_response(
            'stockPrediction/stockPrediction.html',
                {'user': request.user,
                 'time':time,
                 }
        )





from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import Company
from .models import Oneyearstock
from .models import Onedaystock
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib import  auth
from django.contrib.auth.forms import UserCreationForm
import json
import collections
import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object


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
    company_name = 'GOOG'
    #result = (Oneyearstock.objects.raw('SELECT time,name,price FROM stockPrediction_oneyearstock WHERE name = "YHOO" '))
    result = Onedaystock.objects.filter(name='YHOO')
    rowlist = []
    for row in result:
        d = collections.OrderedDict()
        d["time"] = row.time
        d['name'] = 'YHOO'
        d['price'] = row.price
        d['volume'] = row.volume
        rowlist.append(d)
    j = json.dumps(rowlist,cls=DateTimeEncoder)
    print j
    return JsonResponse(j,safe=False)

def stock_prediction(request):
    if(request.method == 'POST'):
        print 'Post'
    else:
        print request.user.username
        return render_to_response(
            'stockPrediction/stockPrediction.html',
                {'user': request.user}
        )





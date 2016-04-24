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


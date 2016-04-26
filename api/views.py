from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stockPrediction.models import *
from .serializers import *



# Create your views here.


@api_view(['GET'])


def stocktestjson(request):
    companys  = Company.objects.all()
    serializers = CompanySerializer(companys,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def oneyearstock(request):
    company_name = str(request.GET.get('name'))
    stocks = Oneyearstock.objects.filter(name=company_name)
    serializers=OneyearstockSerializer(stocks,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def onedaystock(request):
    company_name = str(request.GET.get('name'))
    stocks = Onedaystock.objects.filter(name=company_name)
    serializers=OnedaystockSerializer(stocks,many=True)
    return Response(serializers.data)

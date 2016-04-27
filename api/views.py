from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
import json
import collections

from stockPrediction.models import *
from .serializers import *

from prediction import *


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

@api_view(['GET'])
def latestOneyearstock(request):
    stocks = Oneyearstock.objects.raw('select * from stockPrediction_oneyearstock where time = (select min(time) from stockPrediction_oneyearstock )')
    #stocks = Oneyearstock.objects.all()
    serializers = OneyearstockSerializer(stocks,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def highestLastnDays(request):
    company_name = str(request.GET.get('name'))
    days = int(request.GET.get('day'))
    #print days
    stocks = Oneyearstock.objects.raw('select * from stockPrediction_oneyearstock where name= %s and datediff(CURDATE(),time) <= %s ORDER BY CLOSE DESC limit 1',[company_name,days])
    serializers = OneyearstockSerializer(stocks,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def averagestock(request):
    company_name = str(request.GET.get('name'))
    cursor = connection.cursor()
    cursor.execute('select avg(close) from stockPrediction_oneyearstock WHERE name = %s',[company_name])
    average = cursor.fetchone()[0]
    rowlist =[]
    d = collections.OrderedDict()
    d["name"] = company_name
    d["price"] = average
    rowlist.append(d)
    return Response(rowlist)

@api_view(['GET'])
def lowestprice(request):
    cursor = connection.cursor()
    cursor.execute('select min(close),NAME FROM stockPrediction_oneyearstock GROUP BY NAME ')
    rowlist = []
    for row in cursor.fetchall():
        d = collections.OrderedDict()
        d["name"] = row[1]
        d["price"] = row[0]
        rowlist.append(d)
    return Response(rowlist)

@api_view(['GET'])
def lesserthan(request):
    company_name = str(request.GET.get('name'))
    cursor = connection.cursor()
    cursor.execute('select min(close) from stockPrediction_oneyearstock WHERE NAME = %s',[company_name])
    price = cursor.fetchone()[0]
    cursor.execute('select DISTINCT C.id,C.name FROM stockPrediction_oneyearstock as Y,stockPrediction_company as C WHERE Y.name=C.name and CLOSE < %s',[price])
    rowlist = []
    for row in cursor.fetchall():
        d = collections.OrderedDict()
        d["id"] = row[0]
        d["name"] = row[1]
        rowlist.append(d)
    return Response(rowlist)

@api_view(['GET'])
def indicator(request):
    company_name = str(request.GET.get('name'))
    indicatorname = str(request.GET.get('indicator'))
    min_or_days = str(request.GET.get('timescale'))
    print min_or_days
    rowlist = indicatorCalculate(company_name, indicatorname, min_or_days)
    return Response(rowlist)

@api_view(['GET'])
def dayPrediction(request):
    company_name = str(request.GET.get('name'))
    strategy = str(request.GET.get('strategy'))
    days = int(request.GET.get('days'))
    rowlist = daystockPrediction(company_name, strategy, days)
    return Response(rowlist)

@api_view(['GET'])
def minPrediction(request):
    company_name = str(request.GET.get('name'))
    strategy = str(request.GET.get('strategy'))
    minutes = int(request.GET.get('minutes'))
    rowlist = minstockPrediction(company_name,strategy,minutes)

    return Response(rowlist)



























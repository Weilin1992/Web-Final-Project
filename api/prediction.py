import collections
from stockPrediction.models import *

from django.db import connection


def daystockPrediction(company_name,strategy,days):
    """

    :param company_name:the name of the company you want to predict
    :param strategy:machine learning algrithom
    :param days:the number of days to predict, days = 5 means we are going to predict next 5 days stock price
    :return:a list of dict

    this is just an function to get the stock price, you have to define your own ml class to do prediction
    and remember your class have to receive days, strategy, and company_name as property or param
    and all you have to return is a list of dict, as it shows below, the list should contain both historical
    stock price and the next 5 days price
    """
    rowlist = []
    cursor = connection.cursor()
    cursor.execute('select * from stockPrediction_oneyearstock where name = %s',[company_name])
    for row in cursor.fetchall():
        d = collections.OrderedDict()
        #d["id"] = row[0]
        d["name"] = company_name
        d["pirce"] = row[4]
        d["time"] = row[2]
        rowlist.append(d)

    return rowlist

def minstockPrediction(company_name,strategy,minutes):
    """
    almost the same with daystockPrediction
    :param company_name:
    :param strategy:
    :param minutes:
    :return: a list of dict

    """
    rowlist = []
    ###
    cursor = connection.cursor()
    cursor.execute('select * from stockPrediction_onedaystock where name = %s',[company_name])
    for row in cursor.fetchall():
        d = collections.OrderedDict()
        #d["id"] = row[0]
        d["name"] = company_name
        d["pirce"] = row[3]
        d["time"] = row[2]
        rowlist.append(d)
    ###

    return rowlist

def indicatorCalculate(company_name, indicatorname, min_or_days):


    """
    this is the function to get the indicator, their should be long term indicators and short term
    indicators, you have to define your own class, calculate the indicator and return a list of dict
    which contains name,time,and price that can be used to draw a chart

    :param company_name: company_name:string
    :param indicatorname: the name of the indicator,string
    :param min_or_days: long term or short term,string
    :return: a list of dict
    """
    rowlist = []
    cursor = connection.cursor()
    cursor.execute('select * from stockPrediction_onedaystock where name = %s',[company_name])
    for row in cursor.fetchall():
        d = collections.OrderedDict()
        #d["id"] = row[0]
        d["name"] = company_name
        d["pirce"] = row[3]
        d["time"] = row[2]
        rowlist.append(d)
    return rowlist

















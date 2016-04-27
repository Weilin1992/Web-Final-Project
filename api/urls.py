from django.conf.urls import patterns,url
from . import views

urlpatterns = [
    url(r'^lessthan/$',views.lesserthan,name='lessstock'),
    url(r'^lowest/$',views.lowestprice,name='loweststock'),
    url(r'^average/$',views.averagestock,name='averagestock'),
    url(r'^highestLastnDays/$',views.highestLastnDays,name='highestLastnDays'),
    url(r'^latestOneyearstock/$',views.latestOneyearstock,name='lastestoneyearstock'),
    url(r'^onedaystock/$',views.onedaystock,name='onedaystock'),
    url(r'^oneyearstock/$',views.oneyearstock,name='oneyearstock'),
    url(r'^stocktestjson/$',views.stocktestjson,name='stocktestjson'),
]
from django.conf.urls import patterns,url
from . import views

urlpatterns = [
    url(r'^highestLastnDays/$',views.highestLastnDays,name='highestLastnDays'),
    url(r'^latestOneyearstock/$',views.latestOneyearstock,name='lastestoneyearstock'),
    url(r'^onedaystock/$',views.onedaystock,name='onedaystock'),
    url(r'^oneyearstock/$',views.oneyearstock,name='oneyearstock'),
    url(r'^stocktestjson/$',views.stocktestjson,name='stocktestjson'),
]
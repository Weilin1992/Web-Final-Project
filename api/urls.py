from django.conf.urls import patterns,url
from . import views

urlpatterns = [
    url(r'^onedaystock/$',views.onedaystock,name='onedaystock'),
    url(r'^oneyearstock/$',views.oneyearstock,name='oneyearstock'),
    url(r'^stocktestjson/$',views.stocktestjson,name='stocktestjson'),
]
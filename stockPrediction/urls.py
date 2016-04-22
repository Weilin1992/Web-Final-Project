from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$',views.register_user,name= 'register_user'),
    url(r'^register_success/$',views.register_success,name='register_success'),
    url(r'^$', views.index, name='index'),
]
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$',views.login, name='login'),
    url(r'^loggedin/$',views.loggedin, name='loggedin'),
    url(r'^auth/$',views.auth_view,name='auth_view'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^invalid/$',views.invalid_login,name='invalid'),
    url(r'^register_success/$',views.register_success,name='register_success'),
    url(r'^register/$',views.register_user,name='register_user'),
    url(r'^$', views.index, name='index'),
]
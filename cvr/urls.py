from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='cvr/home.html'), name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'cvr/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name': 'cvr/logged_out.html'}, name='logout'),
    url(r'^index/', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
]
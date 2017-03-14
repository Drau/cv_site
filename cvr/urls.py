from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'cvr/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name': 'cvr/logged_out.html'}, name='logout'),
    url(r'^update_profile/', views.update_profile, name='update_profile'),
    url(r'^profile/(?P<profile_id>.*)$', views.profile, name='profile'),
    url(r'^register/', views.register, name='register'),
    url(r'^cv_list/', views.cv_list, name='cv_list'),
    url(r'^download/(?P<path>.*)$', views.download, name='download'),
]
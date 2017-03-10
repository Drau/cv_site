import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from annoying.functions import get_object_or_None
from django.forms.models import model_to_dict

from .forms import UserForm, ProfileForm
from .models import Profile

@login_required
def update_profile(request):
    profile = get_object_or_None(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cvs/profile')
    else:
        if request.user.is_staff:
            return HttpResponseRedirect('/cvs/')
        if profile is None:
            profile = Profile(user=request.user, image="images/default.jpg")
            profile.save()
        form = ProfileForm(instance=profile)
        return render(request, 'cvr/update_profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cvs/login')
    else:
        form = UserForm()
    return render(request, 'cvr/register.html', {'form': form})

def home(request):
    if request.user.is_authenticated():
        profile = get_object_or_None(Profile, user=request.user)
        if profile is None:
            return HttpResponseRedirect('/cvs/update_profile')
    return render(request, 'cvr/home.html')

@login_required()
def profile(request):
    profile = None
    if request.user.is_authenticated():
        profile = get_object_or_None(Profile, user=request.user)
        if profile is None:
            return HttpResponseRedirect('/cvs/update_profile')
    return render(request, 'cvr/profile.html', {'profile': profile})

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        return HttpResponseRedirect('/cvs/profile')
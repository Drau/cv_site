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
def profile(request):
    profile = get_object_or_None(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cvs')
    else:
        if request.user.is_staff:
            return HttpResponse('You are staff member , go away !')
        else:
            if profile is None:
                profile = Profile(user=request.user)
                profile.save()
            form = ProfileForm(instance=profile)
            return render(request, 'cvr/profile.html', {'form': form})


def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cvs/login')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, 'cvr/register.html', {'form': form})


def home(request):
    profile = None
    if request.user.is_authenticated():
        profile = get_object_or_None(Profile, user=request.user)
        if profile is None:
            return HttpResponseRedirect('/cvs/profile')
    return render(request, 'cvr/home.html', {'profile': profile})


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        return HttpResponseRedirect('/cvs/profile')
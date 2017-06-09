import os
import mimetypes

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect,  Http404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from annoying.functions import get_object_or_None
from django.forms.models import model_to_dict

from .forms import UserForm, ProfileForm
from .models import Profile
from password_reset import views as password_views

@login_required
def update_profile(request,profile_id):
    profile = get_object_or_None(Profile, pk=profile_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cvs/profile/{}'.format(profile.id))
    else:
        if (request.user.is_staff) or (str(request.user.profile.id) == profile_id):
            if profile is None:
                profile = Profile(user=request.user, image="images/default.jpg")
                profile.save()
            form = ProfileForm(instance=profile)
            return render(request, 'cvr/update_profile.html', {'form': form, 'profile': profile})
        else:
            return HttpResponseRedirect('/cvs/')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cvs/login')
    else:
        form = UserForm()
    return render(request, 'cvr/register.html', {'form': form})

@login_required()
def home(request):
    # updating allowed profiles -> Stay at home page
    if request.method=='POST':
        data = request.POST.getlist('approve')
        for profile_id in data:
            profile = Profile.objects.get(pk=profile_id)
            profile.is_approved = True
            profile.save()
        profiles = Profile.objects.filter(is_approved=False, user__is_staff=False).exclude(first_name__exact='')
        return render(request, 'cvr/home.html', {'profiles': profiles})
    # GET request
    else:
        # If regular user
        if  not request.user.is_staff and not request.user.profile.is_privledged:
            profile = get_object_or_None(Profile, user=request.user)
            # If no CV exists -> Force profile update
            if not profile.cv:
                return HttpResponseRedirect('/cvs/profile/{}/update_profile'.format(request.user.profile.id))
            # If CV exists -> move to profile page
            else:
                return HttpResponseRedirect('/cvs/profile/{}'.format(request.user.profile.id))
        # If is_privledged or admin(is_staff)
        else:
            # If user is provledged -> Move to cv_list
            if request.user.profile.is_privledged:
                return HttpResponseRedirect('/cvs/cv_list')
            # If user is admin -> Move to home page
            elif request.user.is_staff:
                profiles = Profile.objects.filter(is_approved=False, user__is_staff=False).exclude(first_name__exact='')
                return render(request, 'cvr/home.html', {'profiles': profiles})


@login_required()
def cv_list(request):
    is_mobile = any([i in request.META.get('HTTP_USER_AGENT','').lower() for i in ["iphone", "mobile", "android"]])
    if not request.user.is_staff and not request.user.profile.is_privledged:
         return render(request, 'cvr/home.html')
    else:
        users = User.objects.all()
        return render(request, 'cvr/cv_list.html', {'users': users, 'is_mobile': is_mobile})


@login_required()
def profile(request, profile_id):
    is_mobile = any([i in request.META.get('HTTP_USER_AGENT','').lower() for i in ["iphone", "mobile", "android"]])
    profile = None
    if request.user.is_authenticated():
        profile = get_object_or_None(Profile, pk=profile_id)
        if profile is None:
            if request.user.is_staff or request.user.profile.is_privledged:
                return HttpResponseRedirect('/cvs/home')
            else:    
                return HttpResponseRedirect('/cvs/profile/{}/update_profile'.format(request.user.profile.id))
        local_user = User.objects.get(profile__first_name=profile.first_name)
    return render(request, 'cvr/profile.html', {'profile': profile, 'is_mobile': is_mobile, 'local_user': local_user})

@login_required()
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Description'] = 'File Transfer'
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        # else:
        #     raise Http404("לא נמצאו קורות חיים במערכת.")
    else:
        return HttpResponseRedirect('/cvs/profile')

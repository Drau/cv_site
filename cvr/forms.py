from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


from .models import Profile


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'cv', 'free_text']
        labels = {
            'first_name': 'שם פרטי',
            'last_name': 'שם משפחה',
            'cv': 'קורות חיים',
            'free_text': 'טקסט חופשי',
        }
        help_texts = {
            # 'first_name': 'שם פרטי',
            # 'last_name': 'שם משפחה',
            # 'cv': 'קורות חיים',
            # 'free_text': 'טקסט חופשי',
        }
        error_messages = {
        #     'password2': {
        #         'password_mismatch': "סיסמאות אינן תואמות"),
        #     },
        }

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        if commit:
            profile.save()
        return profile

class UserForm(ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="סיסמא")
    password2 = forms.CharField(widget=forms.PasswordInput, label="אימות סיסמא")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        labels = {
            'username': 'שם משתמש',
            'email': 'אימייל',
        }
        help_texts = {
            # 'username': 'שם משתמש',
            # 'email': 'אימייל'),
        }
        error_messages = {
        #     'password2': {
        #         'password_mismatch': "סיסמאות אינן תואמות"),
        #     },
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user
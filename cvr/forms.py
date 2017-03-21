from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


from .models import Profile


class ProfileForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="שם פרטי")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="שם משפחה")
    cv = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}), label="קורות חיים", required=False)
    # cv = forms.ClearableFileInput()
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}), label="תמונה", required=False )
    free_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="טקסט חופשי", required=False )
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'cv', 'image', 'free_text']
        labels = {
        }
        help_texts = {
        }
        error_messages = {
        }

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        if commit:
            profile.save()
        return profile

class UserForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="שם משתמש")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="סיסמא")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="אימות סיסמא")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label="אימייל")
    
    error_messages = {
        'password_mismatch': "סיסמאות אינן תואמות",
    }

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        help_texts = {
        }
        error_messages = {
            'password2': {
                'password_mismatch': "סיסמאות אינן תואמות",
            },
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
            profile = Profile.objects.create(user=user, image="images/default.jpg")
            profile.save()
        return user
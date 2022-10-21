from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms import ModelForm
from django.http import HttpResponse


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'username', 'email', 'profile_pic', 'year', 'semester',
            'school',
            'course', 'is_staff',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'username', 'email', 'profile_pic', 'year', 'semester',
            'school',
            'course', 'is_staff', ]


class UserUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'username', 'email', 'profile_pic', 'year', 'semester',
                  'school',
                  'course', 'is_staff', ]


class UpdateProfilePic(forms.Form):
    image = forms.ImageField()

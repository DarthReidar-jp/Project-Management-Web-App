from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    country = forms.CharField(max_length=30, required=True, help_text='Required.')
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'country', 'password1', 'password2']
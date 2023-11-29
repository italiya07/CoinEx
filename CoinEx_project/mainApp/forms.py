from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Tweet

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # Add custom fields as needed

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # Add custom fields as needed

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}))
    
    
class TweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder": "Enter your Tweet!!",
            "class": "form-control"
        }),
        label=""
    )

    class Meta:
        model = Tweet
        exclude = ("user",)

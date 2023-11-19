from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class CustomUserForm(UserCreationForm):
    id_or_photo = forms.ImageField(required=True, label='Upload a valid photo ID')

    # def clean_id_or_photo(self):
    #     id_or_photo = self.cleaned_data.get('id_or_photo')

    #     if not id_or_photo:
    #         raise forms.ValidationError("This field is required.")

    #     # Add additional validation logic here if needed

    #     return id_or_photo

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'id_or_photo']  # Add custom fields as needed

class CustomUserChangeForm(UserChangeForm):
    id_or_photo = forms.ImageField(required=False, label='Upload a valid photo ID')

    # def clean_id_or_photo(self):
    #     id_or_photo = self.cleaned_data.get('id_or_photo')

    #     if not id_or_photo:
    #         raise forms.ValidationError("This field is required.")

    #     # Add additional validation logic here if needed

    #     return id_or_photo
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'id_or_photo']  # Add custom fields as needed

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}))


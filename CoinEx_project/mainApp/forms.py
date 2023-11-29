from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Tweet
from .models import User, NFT


class CustomUserForm(UserCreationForm):
    id_or_photo = forms.ImageField(required=True, label="Upload a valid photo ID")

    # def clean_id_or_photo(self):
    #     id_or_photo = self.cleaned_data.get('id_or_photo')

    #     if not id_or_photo:
    #         raise forms.ValidationError("This field is required.")

    #     # Add additional validation logic here if needed

    #     return id_or_photo

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "id_or_photo",
        ]  # Add custom fields as needed


class CustomUserChangeForm(UserChangeForm):
    id_or_photo = forms.ImageField(required=False, label="Upload a valid photo ID")

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "id_or_photo",
        ]


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

class ContactForm(forms.Form):
    user_name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    query = forms.CharField(widget=forms.Textarea, label='Your Query')


class BuyCrypto(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    stripeToken = forms.CharField(widget=forms.HiddenInput())


class TransactionFilterForm(forms.Form):
    TYPE = [("BUY", "Buy"), ("SELL", "Sell")]

    transaction_type = forms.ChoiceField(
        label="Transaction Type", choices=[("", "All")] + TYPE, required=False
    )

    stock_symbol = forms.CharField(
        label="Search by Symbol",
        max_length=10,
        required=False,
        widget=forms.TextInput(),
    )

    start_date = forms.DateField(
        label="Start Date",
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
    )

    end_date = forms.DateField(
        label="End Date", required=False, widget=forms.TextInput(attrs={"type": "date"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stock_symbol"].widget.attrs.update(
            {"placeholder": "Symbol to search"}
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date cannot be greater than end date.")


class NFTForm(forms.ModelForm):
    class Meta:
        model = NFT
        fields = '__all__'

class BuyNFT(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    stripeToken = forms.CharField(widget=forms.HiddenInput())


class SellStockForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    stock_symbol = forms.CharField(widget=forms.HiddenInput())


class SellNFTForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    nft_symbol = forms.CharField(widget=forms.HiddenInput())

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import FearAndGreedIndex, News, Cryptocurrency
from .forms import CustomUserForm,  EmailAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def apis(change='USD'):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start': 1,
    'limit': 50,
    'convert': change
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '94cc259d-0784-4fb2-bd01-4b0f9dc3926f',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        # print(data)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        # print(e)
        return e

def index(request):

    main_data = apis()
    # print(main_data['data'])
    data = {
        "cryptos": main_data['data'],
        "currency" : 'USD'
    }
    # print("\n we are taking context\n")
    # print(data)

    return render(request, 'CoinEx_Index/index.html', context=data)
    # return render(request, 'CoinEx_Index/index.html', context=context)

@login_required(login_url='login')
def exchange(request, currency_symbol):

    main_data = apis(currency_symbol)
    # print(main_data['data'])
    data = {
        "cryptos": main_data['data'], 
        "currency" : currency_symbol
    }
    # print("\n we are taking context\n")
    # print(data)

    return render(request, 'CoinEx_Index/index.html', context=data)


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        # form = CustomUserForm(request.POST)

        if form.is_valid():
            print("Befor save user")
            print(form, "*******")
            user = form.save()
            # form.save()
            print("after save user")
            # login(request, user)
            return redirect('login')
            
    else:
        form = CustomUserForm()
    return render(request, 'CoinEx_Index/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_authenticated:
                print("user is authenticated", user.is_authenticated)
            else:
                print("not authenticated", user.is_authenticated)
            django_login(request, user)

            if user.is_authenticated:
                print("user is authenticated", user.is_authenticated)
            return redirect('index')  # Redirect to a success page
    else:
        form = EmailAuthenticationForm()
    return render(request, 'CoinEx_Index/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect("/")

def crypto_highlights(request):
    all_cryptos = Cryptocurrency.objects.all()
    return render(request, 'CoinEx_Index/crypto_highlights.html', {'all_cryptos': all_cryptos})

def fear_and_greed_index(request):
    all_indexes = FearAndGreedIndex.objects.all()
    return render(request, 'CoinEx_Index/fear_and_greed_index.html', {'all_indexes': all_indexes})

def news_list(request):
    all_news = News.objects.all()
    return render(request, 'mainApp/news_list.html', {'all_news': all_news})





# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import Crypto, FearAndGreedIndex, News, Cryptocurrency
from .forms import CustomUserForm,  EmailAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as django_login, authenticate

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
    print(main_data['data'])
    data = {
        "cryptos": main_data['data'],
        "currency" : 'USD'
    }
    print("\n we are taking context\n")
    print(data)

    return render(request, 'CoinEx_Index/index.html', context=data)
    # return render(request, 'CoinEx_Index/index.html', context=context)

def exchange(request, currency_symbol):

    main_data = apis(currency_symbol)
    print(main_data['data'])
    data = {
        "cryptos": main_data['data'], 
        "currency" : currency_symbol
    }
    print("\n we are taking context\n")
    print(data)

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
            django_login(request, user)
            return redirect('index')  # Redirect to a success page
    else:
        form = EmailAuthenticationForm()
    return render(request, 'CoinEx_Index/login.html', {'form': form})

def dashboard(request):
    # Retrieve top 5 cryptocurrencies for the highlight box
    top_cryptos = Crypto.objects.all()[:5]

    # Retrieve latest 5 news for the highlight box
    latest_news = News.objects.all()[:5]

    # Retrieve the latest Fear & Greed Index value
    latest_index = FearAndGreedIndex.objects.latest('date')

    return render(request, 'mainApp/dashboard.html', {'top_cryptos': top_cryptos, 'latest_news': latest_news, 'latest_index': latest_index})


def crypto_list(request):
    all_cryptos = Crypto.objects.all()
    return render(request, 'mainApp/crypto_list.html', {'all_cryptos': all_cryptos})

def fear_and_greed_index(request):
    all_indexes = FearAndGreedIndex.objects.all()
    return render(request, 'mainApp/fear_and_greed_index.html', {'all_indexes': all_indexes})

def news_list(request):
    all_news = News.objects.all()
    return render(request, 'mainApp/news_list.html', {'all_news': all_news})





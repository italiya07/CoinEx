# Create your views here.
from datetime import datetime

import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import FearAndGreedIndex, News, Cryptocurrency, ContactUs
from .forms import CustomUserForm, EmailAuthenticationForm, ContactForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from datetime import datetime


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def apis(change="USD"):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {"start": 1, "limit": 50, "convert": change}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "94cc259d-0784-4fb2-bd01-4b0f9dc3926f",
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

def extract_top_gainers_and_losers(main_data, limit=5):
    # Extract the list of cryptocurrencies from main_data
    cryptocurrencies = main_data.get('data', [])

    # Sort the cryptocurrencies based on percent_change_24h in descending order
    sorted_cryptos = sorted(cryptocurrencies, key=lambda x: x['quote']['USD']['percent_change_24h'], reverse=True)

    # Extract top gainers and losers with only required information
    top_gainers = [
        {
            'name': crypto['name'],
            'symbol': crypto['symbol'],
            'price': round(crypto['quote']['USD']['price'], 3),
            'percent_change_24h': round(crypto['quote']['USD']['percent_change_24h'], 3)
        }
        for crypto in sorted_cryptos[:limit]
    ]

    top_losers = [
        {
            'name': crypto['name'],
            'symbol': crypto['symbol'],
            'price': round(crypto['quote']['USD']['price'], 3),
            'percent_change_24h': round(crypto['quote']['USD']['percent_change_24h'], 3)
        }
        for crypto in sorted_cryptos[-limit:]
    ]

    return top_gainers, top_losers

def extract_recently_added(main_data, limit=5):
    try:
        # Extract the list of cryptocurrencies from main_data
        cryptocurrencies = main_data.get('data', [])

        # Sort the cryptocurrencies based on the date_added in descending order
        sorted_cryptos = sorted(cryptocurrencies, key=lambda x: x['date_added'], reverse=True)

        # Extract recently added cryptocurrencies with only required information
        recently_added = [
            {
                'name': crypto['name'],
                'symbol': crypto['symbol'],
                'price': round(crypto['quote']['USD']['price'], 3),
                'date_added': datetime.strptime(crypto['date_added'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%B %d, %Y')
            }
            for crypto in sorted_cryptos[:limit]
        ]

        return recently_added
    except Exception as e:
        # Handle exceptions, e.g., data format issues
        print(f"Error in processing API data: {e}")
        return None

def index(request):
    main_data = apis()
    print(main_data['data'])

    top_gainers, top_losers = extract_top_gainers_and_losers(main_data)

    recently_added = extract_recently_added(main_data)

    data = {
        "cryptos": main_data['data'],
        "currency" : 'USD',
        "top_gainers": top_gainers,
        "top_losers": top_losers,
        "recently_added": recently_added
    }
    # print("\n we are taking context\n")
    # print(data)
    # print("-------->", len(main_data))

    return render(request, 'CoinEx_Index/index.html', context=data)

def extract_top_cryptos_by_rank(main_data, limit=10):
    try:
        # Extract the list of cryptocurrencies from main_data
        cryptocurrencies = main_data.get('data', [])

        # Sort the cryptocurrencies based on the cmc_rank in ascending order
        sorted_cryptos = sorted(cryptocurrencies, key=lambda x: x['cmc_rank'])

        # Extract top cryptocurrencies based on CMC rank with only required information
        top_cryptos = [
            {
                'name': crypto['name'],
                'symbol': crypto['symbol'],
                'price': round(crypto['quote']['USD']['price'], 3)
            }
            for crypto in sorted_cryptos[:limit]
        ]

        return top_cryptos
    except Exception as e:
        # Handle exceptions, e.g., data format issues
        print(f"Error in processing API data: {e}")
        return None


def extract_trending_latest(main_data, limit=10):
    try:
        # Extract the list of cryptocurrencies from main_data
        cryptocurrencies = main_data.get('data', [])

        # Sort the cryptocurrencies based on the volume_24h in descending order
        sorted_cryptos = sorted(cryptocurrencies, key=lambda x: x['quote']['USD']['volume_24h'], reverse=True)

        # Extract trending latest cryptocurrencies based on volume with only required information
        trending_latest = [
            {
                'name': crypto['name'],
                'symbol': crypto['symbol'],
                'price': round(crypto['quote']['USD']['price'], 3),
                'volume_24h': int(crypto['quote']['USD']['volume_24h'])
            }
            for crypto in sorted_cryptos[:limit]
        ]

        return trending_latest
    except Exception as e:
        # Handle exceptions, e.g., data format issues
        print(f"Error in processing API data: {e}")
        return None


def crypto_highlights(request):
    main_data = apis()
    top_cryptos = extract_top_cryptos_by_rank(main_data, 10)
    top_gainers, top_losers = extract_top_gainers_and_losers(main_data, 10)
    recently_added = extract_recently_added(main_data, 10)
    trending_latest = extract_trending_latest(main_data, 10)

    # Retrieve latest 5 news based on published date
    latest_news = News.objects.order_by('-published_date')[:10]

    # Retrieve the latest Fear & Greed Index value
    latest_fg_index = FearAndGreedIndex.objects.latest('date')

    all_fg_indexes = FearAndGreedIndex.objects.all()

    # Create a context dictionary with the data
    context = {
        'top_cryptos': top_cryptos,
        'top_gainers': top_gainers,
        'top_losers': top_losers,
        'recently_added': recently_added,
        'trending_latest': trending_latest,
        "latest_fg_index": latest_fg_index,
        "latest_news": latest_news,
        "all_fg_indexes": all_fg_indexes
    }
    print(context)
    # Render the template with the context
    return render(request, 'CoinEx_Index/crypto_highlights.html', context)


@login_required(login_url="login")
def exchange(request, currency_symbol):
    main_data = apis(currency_symbol)
    # print(main_data['data'])
    data = {"cryptos": main_data["data"], "currency": currency_symbol}
    # print("\n we are taking context\n")
    # print(data)

    return render(request, "CoinEx_Index/index.html", context=data)


def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST, request.FILES)
        # form = CustomUserForm(request.POST)

        if form.is_valid():
            print("Befor save user")
            print(form, "*******")
            user = form.save()
            # form.save()
            print("after save user")
            # login(request, user)
            return redirect("login")

    else:
        form = CustomUserForm()
    return render(request, "CoinEx_Index/register.html", {"form": form})


def login(request):
    if request.method == "POST":
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
            return redirect("index")  # Redirect to a success page
    else:
        form = EmailAuthenticationForm()
    return render(request, "CoinEx_Index/login.html", {"form": form})


def logout(request):
    auth.logout(request)
    return redirect("/")


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            contact_submission = ContactUs(
                customer_name=form.cleaned_data['user_name'],
                customer_email=form.cleaned_data['email'],
                query=form.cleaned_data['query'],
                created_at = datetime.now()
            )
            contact_submission.save()
            return HttpResponse('contact_success')  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, 'CoinEx_Index/contact_us2.html', {'form': form})


def crypto_highlights(request):
    all_cryptos = Cryptocurrency.objects.all()
    return render(
        request, "CoinEx_Index/crypto_highlights.html", {"all_cryptos": all_cryptos}
    )


def fear_and_greed_index(request):
    all_indexes = FearAndGreedIndex.objects.all()
    return render(
        request, "CoinEx_Index/fear_and_greed_index.html", {"all_indexes": all_indexes}
    )


def news_list(request):
    all_news = News.objects.all()
    return render(request, "CoinEx_Index/news_list.html", {"all_news": all_news})


def calculate_topness(crypto):
    # Define weights for each factor
    weight_change = 0.4
    weight_volume = 0.3
    weight_market_cap = 0.3

    # Convert Decimal values to float for calculation
    change = float(crypto.twenty_four_hour_change)
    volume = float(crypto.volume)
    market_cap = float(crypto.market_cap)

    # Calculate the topness score using the weights
    topness_score = (
        change * weight_change + volume * weight_volume + market_cap * weight_market_cap
    )

    return topness_score
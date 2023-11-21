# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import FearAndGreedIndex, News, Cryptocurrency
from .forms import CustomUserForm,  EmailAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as django_login, authenticate

def index(request):
    cryptos = Cryptocurrency.objects.all()

    # Calculate topness scores for all cryptocurrencies
    cryptos_with_topness = [
        (crypto, calculate_topness(crypto))
        for crypto in cryptos
    ]

    # Sort cryptocurrencies based on topness scores in descending order
    sorted_cryptos = sorted(cryptos_with_topness, key=lambda x: x[1], reverse=True)

    # Retrieve top 5 cryptocurrencies
    top_cryptos = [crypto for crypto, _ in sorted_cryptos[:5]]

    # Retrieve latest 5 news based on published date
    latest_news = News.objects.order_by('-published_date')[:5]

    # Retrieve the latest Fear & Greed Index value
    latest_index = FearAndGreedIndex.objects.latest('date')

    # Set a static value for testing
    #static_index_value = 35  # You can change this to any value for testing

    context = {
        "cryptos": cryptos,
        "top_cryptos": top_cryptos,
        "latest_news": latest_news,
        #"latest_index": FearAndGreedIndex(value=static_index_value),
        "latest_index": latest_index
    }

    return render(request, 'CoinEx_Index/index.html', context=context)

def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            print("Befor save user")
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

def crypto_highlights(request):
    all_cryptos = Cryptocurrency.objects.all()
    return render(request, 'CoinEx_Index/crypto_highlights.html', {'all_cryptos': all_cryptos})

def fear_and_greed_index(request):
    all_indexes = FearAndGreedIndex.objects.all()
    return render(request, 'CoinEx_Index/fear_and_greed_index.html', {'all_indexes': all_indexes})

def news_list(request):
    all_news = News.objects.all()
    return render(request, 'CoinEx_Index/news_list.html', {'all_news': all_news})

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
    topness_score = (change * weight_change +
                     volume * weight_volume +
                     market_cap * weight_market_cap)

    return topness_score

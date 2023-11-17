# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Crypto, FearAndGreedIndex, News

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


def index(request):

    cryptos = [
        {
            "name": "Bitcoin",
            "Price": 34500,
            "oneHour": "0.27%",
            "oneHourFlag": -1,
            "TwentyFourHour": "0.67",
            "TwentyFourHourFlag": -1,
            "MarketCap": "673,506,667,886",
            "Volume": "17,354,758,340"
        },
        {
            "name": "Ethereum",
            "Price": 2600,
            "oneHour": "0.42%",
            "oneHourFlag": 1,
            "TwentyFourHour": "1.25%",
            "TwentyFourHourFlag": 1,
            "MarketCap": "300,456,789,123",
            "Volume": "10,456,123,789"
        },
        {
            "name": "Solana",
            "Price": 1.23,
            "oneHour": "0.11%",
            "oneHourFlag": -1,
            "TwentyFourHour": "0.75%",
            "TwentyFourHourFlag": -1,
            "MarketCap": "56,789,123,456",
            "Volume": "2,345,678,901"
        },
        {
            "name": "XRP",
            "Price": 155,
            "oneHour": "0.33%",
            "oneHourFlag": 1,
            "TwentyFourHour": "0.85%",
            "TwentyFourHourFlag": 1,
            "MarketCap": "12,345,678,901",
            "Volume": "567,890,123"
        },
        {
            "name": "BNB",
            "Price": 2.45,
            "oneHour": "0.28%",
            "oneHourFlag": 1,
            "TwentyFourHour": "0.92%",
            "TwentyFourHourFlag": 1,
            "MarketCap": "7,890,123,456",
            "Volume": "345,678,901"
        }
    ]

    context = {
        "cryptos": cryptos
    }
    return render(request, 'CoinEx_Index/index.html', context=context)



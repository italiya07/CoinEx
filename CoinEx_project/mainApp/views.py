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


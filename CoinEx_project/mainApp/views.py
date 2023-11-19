# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import Crypto, FearAndGreedIndex, News, Cryptocurrency
from .forms import CustomUserForm,  EmailAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as django_login, authenticate

def index(request):
    cryptos = Cryptocurrency.objects.all()

    context = {
        "cryptos": cryptos
    }
    return render(request, 'CoinEx_Index/index.html', context=context)




def register(request):
    if request.method == 'POST':
        # form = CustomUserForm(request.POST, request.FILES)
        form = CustomUserForm(request.POST)

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



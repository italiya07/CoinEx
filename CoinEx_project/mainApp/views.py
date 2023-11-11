from django.shortcuts import render
from .models import Crypto

def dashboard(request):
    cryptos = Crypto.objects.all()
    return render(request, 'mainApp/dashboard.html', {'cryptos': cryptos})
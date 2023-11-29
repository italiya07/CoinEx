# Create your views here.
from datetime import datetime, timedelta

import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import FearAndGreedIndex, News, Cryptocurrency, ContactUs, Transaction, NFTTransaction, NFT, UserHolding, NFTUserHolding
from .forms import CustomUserForm, EmailAuthenticationForm, ContactForm, BuyCrypto, TransactionFilterForm, BuyNFT, SellStockForm, SellNFTForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from datetime import datetime
import stripe
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

stripe.api_key = settings.STRIPE_PRIVATE_KEY
STRIPE_API_KEY_PUBLIC = "pk_test_51OEx8aKe129QqCJpnFq28V5d9Fr2yW9m6WRlmFbCGXBD76cTmxQ9x6EncAIncsbWDDu1EMWd0hB06ycaFC74sl4O00xNhKpdzc"

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

# Index view to display cryptocurrency data
def index(request):
    main_data = apis()
    print(main_data['data'])

    currency_symbol = 'USD'

    top_gainers, top_losers = extract_top_gainers_and_losers(main_data, currency_symbol)

    recently_added = extract_recently_added(main_data, currency_symbol)

    data = {
        "cryptos": main_data['data'],
        "currency" : currency_symbol,
        "top_gainers": top_gainers,
        "top_losers": top_losers,
        "recently_added": recently_added
    }
    return render(request, 'CoinEx_Index/index.html', context=data)

# Exchange view to display cryptocurrency data for a specific currency
@login_required(login_url="login")
def exchange(request, currency_symbol):
    main_data = apis(currency_symbol)
    top_gainers, top_losers = extract_top_gainers_and_losers(main_data, currency_symbol)

    recently_added = extract_recently_added(main_data, currency_symbol)
    # print(main_data['data'])
    data = {
        "cryptos": main_data['data'],
        "currency": currency_symbol,
        "top_gainers": top_gainers,
        "top_losers": top_losers,
        "recently_added": recently_added
    }
    return render(request, "CoinEx_Index/index.html", context=data)

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


def extract_top_gainers_and_losers(main_data, currency_symbol, limit=5):
    # Extract the list of cryptocurrencies from main_data
    cryptocurrencies = main_data.get('data', [])

    # Sort the cryptocurrencies based on percent_change_24h in descending order
    sorted_cryptos = sorted(cryptocurrencies, key=lambda x: x['quote'][currency_symbol]['percent_change_24h'], reverse=True)

    # Extract top gainers and losers with only required information
    top_gainers = [
        {
            'name': crypto['name'],
            'symbol': crypto['symbol'],
            'price': round(crypto['quote'][currency_symbol]['price'], 3),
            'percent_change_24h': round(crypto['quote'][currency_symbol]['percent_change_24h'], 3)
        }
        for crypto in sorted_cryptos[:limit]
    ]

    top_losers = [
        {
            'name': crypto['name'],
            'symbol': crypto['symbol'],
            'price': round(crypto['quote'][currency_symbol]['price'], 3),
            'percent_change_24h': round(crypto['quote'][currency_symbol]['percent_change_24h'], 3)
        }
        for crypto in sorted_cryptos[-limit:]
    ]

    return top_gainers, top_losers

def extract_recently_added(main_data, currency_symbol, limit=5):
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
                'price': round(crypto['quote'][currency_symbol]['price'], 3),
                'date_added': datetime.strptime(crypto['date_added'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%B %d, %Y')
            }
            for crypto in sorted_cryptos[:limit]
        ]

        return recently_added
    except Exception as e:
        # Handle exceptions, e.g., data format issues
        print(f"Error in processing API data: {e}")
        return None


def extract_top_cryptos_by_rank(main_data, currency_symbol, limit=10):
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
                'price': round(crypto['quote'][currency_symbol]['price'], 3)
            }
            for crypto in sorted_cryptos[:limit]
        ]

        return top_cryptos
    except Exception as e:
        # Handle exceptions, e.g., data format issues
        print(f"Error in processing API data: {e}")
        return None


def extract_trending_latest(main_data, currency_symbol, limit=10):
    try:
        # Extract the list of cryptocurrencies from main_data
        cryptocurrencies = main_data.get('data', [])

        # Sort the cryptocurrencies based on the volume_24h in descending order
        sorted_cryptos = sorted(cryptocurrencies, key=lambda x: x['quote'][currency_symbol]['volume_24h'], reverse=True)

        # Extract trending latest cryptocurrencies based on volume with only required information
        trending_latest = [
            {
                'name': crypto['name'],
                'symbol': crypto['symbol'],
                'price': round(crypto['quote'][currency_symbol]['price'], 3),
                'volume_24h': int(crypto['quote'][currency_symbol]['volume_24h'])
            }
            for crypto in sorted_cryptos[:limit]
        ]

        return trending_latest
    except Exception as e:
        # Handle exceptions, e.g., data format issues
        print(f"Error in processing API data: {e}")
        return None


def crypto_highlights(request, currency):
    main_data = apis(currency)
    currency_symbol = currency
    top_cryptos = extract_top_cryptos_by_rank(main_data, currency_symbol, 10)
    top_gainers, top_losers = extract_top_gainers_and_losers(main_data, currency_symbol, 10)
    recently_added = extract_recently_added(main_data, currency_symbol, 10)
    trending_latest = extract_trending_latest(main_data, currency_symbol, 10)

    # Retrieve latest 5 news based on published date
    latest_news = News.objects.order_by('-published_date')[:10]

    # Retrieve the latest Fear & Greed Index value
    latest_fg_index = FearAndGreedIndex.objects.latest('date')

    # Assuming 'end_date' is today's date
    end_date = timezone.now().date()

    # Calculate the start date by subtracting 30 days from the end date
    start_date = end_date - timedelta(days=30)

    # Retrieve the last 30 days' data
    all_fg_indexes = FearAndGreedIndex.objects.filter(date__range=[start_date, end_date])

    # Create a context dictionary with the data
    context = {
        'top_cryptos': top_cryptos,
        'top_gainers': top_gainers,
        'top_losers': top_losers,
        'recently_added': recently_added,
        'trending_latest': trending_latest,
        "latest_fg_index": latest_fg_index,
        "latest_news": latest_news,
        "all_fg_indexes": all_fg_indexes,
        'currency_symbol': currency_symbol
    }
    print(context)
    # Render the template with the context
    return render(request, 'CoinEx_Index/crypto_highlights.html', context)

@login_required(login_url="/login/")
def buy_stock(request, stock_symbol, price):
    error_message = ""
    crypto = Cryptocurrency.objects.get(symbol=stock_symbol)

    new_price_type = type(crypto.price)
    new_price_val = new_price_type(price)
    crypto.price = new_price_val

    if request.method == "POST":
        form = BuyCrypto(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            crypto = crypto
            total_price = crypto.price * quantity  # Calculate total price

            # Handle Stripe payment
            token = form.cleaned_data["stripeToken"]
            try:
                charge = stripe.Charge.create(
                    amount=int(total_price * 100),  # Amount in cents
                    currency="cad",
                    source=token,
                    description=f"Stock Purchase: {stock_symbol}",
                )

                # Record the transaction
                transaction = Transaction(
                    user=request.user,
                    crypto=crypto,
                    transaction_type="Buy",
                    quantity=quantity,
                    price=total_price,
                )
                transaction.save()

                # Update user holdings
                holding, created = UserHolding.objects.get_or_create(
                    user=request.user, crypto=crypto
                )
                holding.quantity += quantity
                holding.save()

                return redirect("transaction-history")
            except stripe.error.CardError as e:
                error_message = e.error.message
                print(f"Stripe CardError: {error_message}")
    else:
        form = BuyCrypto()

    return render(
        request,
        "CoinEx_Index/buy.html",
        {
            "crypto": crypto,
            "error_message": error_message,
            "PUBLIC_KEY": STRIPE_API_KEY_PUBLIC,
            "form": form,
        },
    )


@login_required(login_url="/login/")
def transaction_history(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by("-timestamp")

    if request.method == "GET":
        form = TransactionFilterForm(request.GET)

        if form.is_valid():
            transaction_type = form.cleaned_data.get("transaction_type")
            stock_symbol = form.cleaned_data.get("stock_symbol")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            if start_date and end_date and start_date > end_date:
                form.add_error(
                    "start_date", "Start date cannot be greater than end date."
                )
            else:
                if transaction_type:
                    transaction_type = transaction_type.capitalize()
                    transactions = transactions.filter(
                        transaction_type=transaction_type
                    )
                if stock_symbol:
                    transactions = transactions.filter(
                        stock__symbol__icontains=stock_symbol
                    )
                if start_date:
                    transactions = transactions.filter(timestamp__gte=start_date)
                if end_date:
                    transactions = transactions.filter(timestamp__lte=end_date)

    items_per_page = 10
    paginator = Paginator(transactions, items_per_page)
    page = request.GET.get("page")

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)
    form = TransactionFilterForm(request.GET)
    return render(
        request,
        "CoinEx_Index/transactionhistory.html",
        {"transactions": transactions, "form": form},
    )

def nft_list(request):
    nfts = NFT.objects.all()
    return render(request, 'CoinEx_Index/nft_list.html', {'nfts': nfts})


@login_required(login_url="/login/")
def buy_nft(request, nft_symbol):
    error_message = ""
    nft = NFT.objects.get(symbol=nft_symbol)
    if request.method == "POST":
        form = BuyNFT(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            nft = nft
            total_price = nft.price * quantity  # Calculate total price

            # Handle Stripe payment
            token = form.cleaned_data["stripeToken"]
            try:
                charge = stripe.Charge.create(
                    amount=int(total_price * 100),  # Amount in cents
                    currency="cad",
                    source=token,
                    description=f"NFT Purchase: {nft_symbol}",
                )

                # Record the transaction
                transaction = NFTTransaction(
                    user=request.user,
                    nft=nft,
                    transaction_type="Buy",
                    quantity=quantity,
                    price=total_price,
                )
                transaction.save()

                # Update user holdings
                holding, created = NFTUserHolding.objects.get_or_create(
                    user=request.user, nft=nft
                )
                holding.quantity += quantity
                holding.save()

                return redirect("nft-transaction-history")
            except stripe.error.CardError as e:
                error_message = e.error.message
                print(f"Stripe CardError: {error_message}")
    else:
        form = BuyNFT()

    return render(
        request,
        "CoinEx_Index/buy_nft.html",
        {
            "nft": nft,
            "error_message": error_message,
            "PUBLIC_KEY": STRIPE_API_KEY_PUBLIC,
            "form": form,
        },
    )


@login_required(login_url="/login/")
def nfttransaction_history(request):
    user = request.user
    transactions = NFTTransaction.objects.filter(user=user).order_by("-timestamp")

    if request.method == "GET":
        form = TransactionFilterForm(request.GET)

        if form.is_valid():
            transaction_type = form.cleaned_data.get("transaction_type")
            nft_symbol = form.cleaned_data.get("nft_symbol")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            if start_date and end_date and start_date > end_date:
                form.add_error(
                    "start_date", "Start date cannot be greater than end date."
                )
            else:
                if transaction_type:
                    transaction_type = transaction_type.capitalize()
                    transactions = transactions.filter(
                        transaction_type=transaction_type
                    )
                if nft_symbol:
                    transactions = transactions.filter(
                        nft__symbol__icontains=nft_symbol
                    )
                if start_date:
                    transactions = transactions.filter(timestamp__gte=start_date)
                if end_date:
                    transactions = transactions.filter(timestamp__lte=end_date)

    items_per_page = 10
    paginator = Paginator(transactions, items_per_page)
    page = request.GET.get("page")

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)
    form = TransactionFilterForm(request.GET)
    return render(
        request,
        "CoinEx_Index/nfttransactionhistory.html",
        {"transactions": transactions, "form": form},
    )

@login_required(login_url="/login/")
def user_holdings(request):
    holdings = UserHolding.objects.filter(user=request.user)
    sell_form = SellStockForm()
    items_per_page = 10
    paginator = Paginator(holdings, items_per_page)
    page = request.GET.get("page")
    try:
        holdings_page = paginator.page(page)
    except PageNotAnInteger:
        holdings_page = paginator.page(1)
    except EmptyPage:
        holdings_page = paginator.page(paginator.num_pages)
    # breakpoint()
    if request.method == "POST":
        sell_form = SellStockForm(request.POST)
        if sell_form.is_valid():
            stock_symbol = sell_form.cleaned_data["stock_symbol"]
            quantity_to_sell = sell_form.cleaned_data["quantity"]
            crypto = Cryptocurrency.objects.get(symbol=stock_symbol)
            holding = holdings.filter(crypto=crypto).first()
            if (
                holding
                and quantity_to_sell > 0
                and quantity_to_sell <= holding.quantity
            ):
                sell_price = crypto.price * quantity_to_sell
                sell_transaction = Transaction(
                    user=request.user,
                    crypto=crypto,
                    transaction_type="Sell",
                    quantity=quantity_to_sell,
                    price=sell_price,
                )
                sell_transaction.save()
                holding.quantity -= quantity_to_sell
                holding.save()
                # request.user.wallet += Decimal(sell_price)
                request.user.save()
                if holding.quantity == 0:
                    holding.delete()
                return redirect("user-holdings")
            else:
                error_message = (
                    "Invalid quantity to sell. Please select a valid quantity."
                )
                sell_form.add_error("quantity", error_message)
    return render(
        request,
        "CoinEx_Index/user_holdings.html",
        {"user": request.user, "holdings": holdings_page, "sell_form": sell_form},
    )

@login_required(login_url="/login/")
def nftuser_holdings(request):
    holdings = NFTUserHolding.objects.filter(user=request.user)
    sell_form = SellNFTForm()
    items_per_page = 10
    paginator = Paginator(holdings, items_per_page)
    page = request.GET.get("page")

    try:
        holdings_page = paginator.page(page)
    except PageNotAnInteger:
        holdings_page = paginator.page(1)
    except EmptyPage:
        holdings_page = paginator.page(paginator.num_pages)
    if request.method == "POST":
        sell_form = SellNFTForm(request.POST)
        if sell_form.is_valid():
            nft_symbol = sell_form.cleaned_data["nft_symbol"]
            quantity_to_sell = sell_form.cleaned_data["quantity"]
            nft = NFT.objects.get(symbol=nft_symbol)
            holding = holdings.filter(nft=nft).first()

            if (
                    holding
                    and quantity_to_sell > 0
                    and quantity_to_sell <= holding.quantity
            ):
                sell_price = nft.price * quantity_to_sell

                sell_transaction = NFTTransaction(
                    user=request.user,
                    nft=nft,
                    transaction_type="SELL",
                    quantity=quantity_to_sell,
                    price=sell_price,
                )
                sell_transaction.save()

                holding.quantity -= quantity_to_sell
                holding.save()


                if holding.quantity == 0:
                    holding.delete()

                return redirect("nft-user-holdings")
            else:
                error_message = (
                    "Invalid quantity to sell. Please select a valid quantity."
                )
                sell_form.add_error("quantity", error_message)
    return render(
        request,
        "CoinEx_Index/nftuserholding.html",
        {"user": request.user, "holdings": holdings_page, "sell_form": sell_form},
    )


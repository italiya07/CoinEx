from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('exchange/<str:currency_symbol>/', views.exchange, name='exchange'),
    path('contact_us/', views.contact_us, name='contact_us'),
    # path('dashboard/', dashboard, name='dashboard'),
    path('crypto_highlights/', views.crypto_highlights, name='crypto_highlights'),
    #path('fear_and_greed/', views.fear_and_greed_index, name='fear_and_greed_index'),
    #path('news/', views.news_list, name='news_list'),
    path('buy_crypto/<str:stock_symbol>/', views.buy_stock, name='buy_crypto'),
    path('transaction_history/', views.transaction_history, name='transaction-history'),
    path('nfts/', views.nft_list, name='nft_list'),
    path('buy_nft/<str:nft_symbol>/', views.buy_nft, name='buy_nft'),
    path('nfttransactionhistory/', views.nfttransaction_history, name='nft-transaction-history')

]
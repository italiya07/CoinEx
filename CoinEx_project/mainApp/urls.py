from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('exchange/<str:currency_symbol>/', views.exchange, name='exchange'),
    path('crypto_highlights/', views.crypto_highlights, name='crypto_highlights'),
    #path('fear_and_greed/', views.fear_and_greed_index, name='fear_and_greed_index'),
    #path('news/', views.news_list, name='news_list'),
]
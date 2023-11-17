from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('crypto/', crypto_list, name='crypto_list'),
    path('fear_and_greed/', fear_and_greed_index, name='fear_and_greed_index'),
    path('news/', news_list, name='news_list'),
]

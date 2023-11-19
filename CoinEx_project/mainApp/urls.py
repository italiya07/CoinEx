from django.urls import path
from .views import dashboard, crypto_list, fear_and_greed_index, news_list

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    # path('dashboard/', dashboard, name='dashboard'),
    # path('crypto/', crypto_list, name='crypto_list'),
    # path('fear_and_greed/', fear_and_greed_index, name='fear_and_greed_index'),
    # path('news/', news_list, name='news_list'),
]
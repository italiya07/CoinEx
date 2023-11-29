# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import FearAndGreedIndex, News, Cryptocurrency,Profile,Tweet
from .forms import CustomUserForm,  EmailAuthenticationForm,TweetForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
def index(request):
    cryptos = Cryptocurrency.objects.all()
    # Retrieve top 5 cryptocurrencies for the highlight box
    top_cryptos = Cryptocurrency.objects.all()[:5]

    # Retrieve latest 5 news for the highlight box
    latest_news = News.objects.all()[:5]

    # Retrieve the latest Fear & Greed Index value
    latest_index = FearAndGreedIndex.objects.latest('date')
    context = {
        "cryptos": cryptos,
        "top_cryptos": top_cryptos,
        "latest_news": latest_news,
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

def community(request):
    profile=request.user.profile
    if request.user.is_authenticated:
        form=TweetForm(request.POST or None)
        if request.method=='POST':
            if form.is_valid():
                tweet=form.save(commit=False)
                tweet.user=request.user
                tweet.save()
                messages.success(request,('Your tweet has been saved!!'))
                return redirect('community')
        tweets=Tweet.objects.all().order_by('-created_at')    
        return render(request,'CoinEx_Index/community.html',{'tweets':tweets,'profile':profile,'form':form})
        
    else:
        tweets=Tweet.objects.all().order_by('-created_at')    
        return render(request,'CoinEx_Index/community.html',{'tweets':tweets,'profile':profile})


def delete_tweet(request, tweet_id):
    if request.method == 'POST':
        tweet_to_delete = get_object_or_404(Tweet, id=tweet_id, user=request.user)
        tweet_to_delete.delete()
        messages.success(request, 'Tweet deleted successfully.')
    return redirect('community')  


# @login_required
def profile_list(request):
    # Get the current user's profile
    # current_user_profile = request.user.profile

    # Exclude the current user's profile from the list
    # profileAll=Profile.objects.all()
    # print(profileAll)
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        context = {
            'profiles': profiles,
            # 'current_user_profile': current_user_profile,
        }
        return render(request, 'CoinEx_Index/profile_list.html', context)
    else:
        messages.success(request,("You must be logged in to view this page!!"))
        login_url = reverse('login')
        return redirect(login_url)
         



def profile_detail(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        current_user_profile = request.user.profile
        tweets=Tweet.objects.filter(user__id=pk)

        if request.method == 'POST':
            action = request.POST.get('follow')

            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
                messages.success(request, f"You have unfollowed {profile.user.first_name}.")
            elif action == 'follow':
                current_user_profile.follows.add(profile)
                messages.success(request, f"You are now following {profile.user.first_name}.")

            current_user_profile.save()

        return render(request, 'CoinEx_Index/profile_detail.html', {'profile': profile, 'current_user_profile': current_user_profile,'tweets':tweets})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('login')
    

      

from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.http import JsonResponse
from .models import Tweet
import random
from .forms import TweetForm

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def tweetlist_view(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    tweets_list = [{"id": qs.id, "content":qs.content, "likes": random.randint(0, 99999)} for qs in queryset]
    data = {
        "isUser": False, 
        "response": tweets_list,
    }
    return JsonResponse(data)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        form.save()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({}, status=201)
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html")

def tweetdetail_view(request, tweet_id, *args, **kwargs):
    data = {}
    try: 
        obj = Tweet.objects.get(id= tweet_id)
        data["id"] = obj.id
        data["content"] = obj.content
        status = 200
    except:
        data["message"] = "Tweet Not Found, you probably entered wrong tweet id"
        status = 404
    
    return JsonResponse(data, status= status)
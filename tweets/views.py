from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def tweetlist_view(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    tweets_list = [qs.serialize() for qs in queryset]
    data = {
        "isUser": False, 
        "response": tweets_list,
    }
    return JsonResponse(data)

def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data = request.POST or None)
    if serializer.is_valid():
        serializer.save(user = request.user)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse({}, status=400)





def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(obj.serialize(), status=201)
    if form.errors:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(form.errors, status=400)
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
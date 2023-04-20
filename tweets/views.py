from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet

# Create your views here.
def tweetlist_view(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    tweets_list = [{"id": qs.id, "content":qs.content} for qs in queryset]
    data = {
        "response": tweets_list
    }
    return JsonResponse(data)


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
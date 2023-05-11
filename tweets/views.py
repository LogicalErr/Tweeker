from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import Tweet
from .forms import TweetForm
from .serializers import (
    TweetSerializer, 
    TweetActionSerializer,
    TweetCreateSerializer,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(["GET"])
def tweet_list_view(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    serializer = TweetSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data = request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(["GET"])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    obj = Tweet.objects.get(pk=tweet_id) or None
    if not obj:
        return Response({}, status=404)
    serializer = TweetSerializer(obj)
    return Response(serializer.data)

@api_view(["DELETE", "POST"])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    obj = Tweet.objects.get(pk=tweet_id) or None
    if not obj:
        return Response({"Tweet not found!"}, status=404)
    elif request.user != obj.user:
        return Response({"message": "You can't delete this tweet"}, status=401)
    obj.delete()
    return Response({}, status=204)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
        actions are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        obj = Tweet.objects.get(pk=tweet_id) or None
        if not obj:
            return Response({"Tweet not found!"}, status=404)
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)            
        elif action == "retweet":
            parent_obj = obj
            new_tweet = Tweet.objects.create(user=request.user, parent=parent_obj, content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
        return Response({"action is succesfully done."}, status=200)

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html")
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
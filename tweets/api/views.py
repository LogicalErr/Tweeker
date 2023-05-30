from django.conf import settings
from ..models import Tweet
from .serializers import (
    TweetSerializer, 
    TweetActionSerializer,
    TweetCreateSerializer,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(["GET"])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    try:
        obj = Tweet.objects.get(id=tweet_id) 
    except:
        obj = None
    if not obj:
        return Response({"message":"Tweet not found"}, status=404)
    serializer = TweetSerializer(obj)
    return Response(serializer.data)

@api_view(["GET"])
def tweet_list_view(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    username = request.GET.get('username')
    if username:
        queryset = queryset.by_username(username)
    return get_paginated_queryset_response(queryset, request)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    data = request.data
    serializer = TweetCreateSerializer(data= data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(["DELETE", "POST"])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    obj = Tweet.objects.get(pk=tweet_id) or None
    if not obj:
        return Response({"message":"Tweet not found!"}, status=404)
    elif request.user != obj.user:
        return Response({"message": "You don't have permission to delete this tweet"}, status=401)
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

def get_paginated_queryset_response(queryset, request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginate_qs = paginator.paginate_queryset(queryset, request)
    serializer = TweetSerializer(paginate_qs, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tweet_feed_view(request, *args, **kwargs):
    user = request.user
    queryset = Tweet.objects.feed(user)
    return get_paginated_queryset_response(queryset, request)
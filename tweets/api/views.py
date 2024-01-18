from tweets.models import Tweet
from tweets.api.serializers import (
    TweetSerializer, 
    TweetActionSerializer,
    TweetCreateSerializer,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework import status 
from rest_framework.views import APIView
from tweets import cache_keys
from django.core.cache import cache


class TweetsListView(APIView):
    @staticmethod
    def get(request):
        cache_key = cache_keys.WEB_TWEETS_LIST_CACHE_KEY
        tweets = cache.get(cache_key)
        if not tweets:
            tweets = Tweet.objects.all()
            cache.set(cache_key, tweets)
        username = request.query_params.get('username')
        if username:
            tweets = tweets.filter(user__username=username)

        return get_paginated_queryset_response(tweets, request)


class TweetDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get(request, tweet_id):
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except Tweet.DoesNotExist:
            return Response({"detail": "The tweet your looking for didn't found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TweetSerializer(tweet)
        return Response(serializer.data)

    @staticmethod
    def delete(request, tweet_id):
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except Tweet.DoesNotExist:
            return Response({"detail": "The tweet your looking for didn't found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user != tweet.user:  # TODO should have a custom permission for this
            return Response({"detail": "You are not allowed to delete this tweet"},
                            status=status.HTTP_401_UNAUTHORIZED)

        tweet.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class TweetCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        serializer = TweetCreateSerializer()
        return Response(serializer.data)

    @staticmethod
    def post(request):
        data = request.data
        serializer = TweetCreateSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class TweetActionView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def like_action(tweet, user):
        tweet.likes.add(user)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def unlike_action(tweet, user):
        tweet.likes.remove(user)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def retweet_action(tweet, user, content):
        if tweet.is_retweet:
            parent_tweet = tweet.parent
        else:
            parent_tweet = tweet
        new_tweet = Tweet.objects.create(user=user, parent=parent_tweet, content=content)
        serializer = TweetSerializer(new_tweet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        serializer = TweetActionSerializer()
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = TweetActionSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            tweet_id: int = data.get("id")
            action: str = data.get("action")
            content: str = data.get("content")

            try:
                tweet = Tweet.objects.get(pk=tweet_id)
            except Tweet.DoesNotExist:
                return Response({"detail": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)

            match action.lower():
                case "like":
                    return self.like_action(tweet, user)
                case "unlike":
                    return self.unlike_action(tweet, user)
                case "retweet":
                    return self.retweet_action(tweet, user, content)
        else:
            return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


def get_paginated_queryset_response(queryset, request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginate_qs = paginator.paginate_queryset(queryset, request)
    serializer = TweetSerializer(paginate_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)

# class TweetDeleteView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def delete(self, request, tweet_id):
#         try:
#             tweet = Tweet.objects.get(id=tweet_id)
#         except Tweet.DoesNotExist:
#             return Response({"message": "tweet not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         if request.user != tweet.user:  # TODO should have a custom permission for this
#             return Response({"message": "You are not allowed to delete this tweet"},
#                             status=status.HTTP_401_UNAUTHORIZED)
#
#         tweet.delete()
#         return Response({}, status=status.HTTP_204_NO_CONTENT)


# class TweetFeedView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     @staticmethod
#     def get(request):
#         user = request.user
#         tweets = Tweet.objects.feed(user)
#         return get_paginated_queryset_response(tweets, request)

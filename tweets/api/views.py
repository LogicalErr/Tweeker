from tweets.models import Tweet
from tweets.api.serializers import (
    TweetSerializer, 
    TweetActionSerializer,
    TweetCreateSerializer,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status 
from rest_framework.views import APIView


class TweetDetailView(APIView):
    def get(self, request, tweet_id):
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except Tweet.DoesNotExist:
            return Response({"message": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TweetSerializer(tweet)
        return Response(serializer.data)


class TweetsListView(APIView):

    def get(self, request):
        username = request.query_params.get('username')
        if username:
            tweets = Tweet.objects.filter(user__username=username)
        else:
            tweets = Tweet.objects.all()
        return get_paginated_queryset_response(tweets, request)


class TweetCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = TweetCreateSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class TweetDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, tweet_id):
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except Tweet.DoesNotExist:
            return Response({"message": "tweet not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user != tweet.user:  # TODO should have a custom permission for this
            return Response({"message": "You are not allowed to delete this tweet"},
                            status=status.HTTP_401_UNAUTHORIZED)

        tweet.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


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

    def post(self, request):
        serializer = TweetActionSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            user = request.user
            tweet_id: int = data.get("id")
            action: str = data.get("action")
            content: str = data.get("content")

            try:
                tweet = Tweet.objects.get(pk=tweet_id)
            except Tweet.DoesNotExist:
                return Response({"message": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)

            match action.lower():
                case "like":
                    return self.like_action(tweet, user)
                case "unlike":
                    return self.unlike_action(tweet, user)
                case "retweet":
                    return self.retweet_action(tweet, user, content)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


def get_paginated_queryset_response(queryset, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginate_qs = paginator.paginate_queryset(queryset, request)
    serializer = TweetSerializer(paginate_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)


class TweetFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tweets = Tweet.objects.feed(user)
        return get_paginated_queryset_response(tweets, request)

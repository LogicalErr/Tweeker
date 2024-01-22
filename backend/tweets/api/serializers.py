from rest_framework import serializers
from tweets.models import Tweet
from django.conf import settings 
# from profiles.serializers import PublicProfileSerializer

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS


class TweetCreateSerializer(serializers.ModelSerializer):
    # user = PublicProfileSerializer(source = "user.profile", read_only = True)
    author = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = ["id", 
                  "author", 
                  "content", 
                  "likes", 
                  "timestamp"]

    @staticmethod
    def get_author(obj: Tweet) -> dict:
        return {'id': obj.user.id, 'username': obj.user.username, 'first_name': obj.user.first_name,
                'last_name': obj.user.last_name}

    @staticmethod
    def get_likes(obj: Tweet) -> int:
        return obj.likes.count()

    @staticmethod
    def validate_content(value: str) -> str:
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is more than {} characters".format(MAX_TWEET_LENGTH))
        if len(value) == 0:
            raise serializers.ValidationError("Content can not be empty!")
        return value


class TweetSerializer(serializers.ModelSerializer):
    # user = PublicProfileSerializer(source = "user.profile", read_only = True)
    author = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = [
                    "id", 
                    "author", 
                    "content", 
                    "likes", 
                    "is_retweet", 
                    "parent",
                    "timestamp"
        ]

    @staticmethod
    def get_author(obj: Tweet) -> dict:
        return {'id': obj.user.id, 'username': obj.user.username, 'first_name': obj.user.first_name,
                'last_name': obj.user.last_name}

    @staticmethod
    def get_likes(obj: Tweet) -> int:
        return obj.likes.count()


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    @staticmethod
    def validate_action(value):
        value = value.lower().strip()
        if value in TWEET_ACTION_OPTIONS:
            return value
        else:
            raise serializers.ValidationError("action not valid")

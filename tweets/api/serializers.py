from rest_framework import serializers
from ..models import Tweet
from django.conf import settings 
from profiles.serializers import PublicProfileSerializer

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source = "user.profile", read_only = True)
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ["user", 
                  "id", 
                  "content", 
                  "likes", 
                  "timestamp"]
        
    def get_likes(self, obj):
        return obj.likes.count()
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is more than {} characters".format(MAX_TWEET_LENGTH))
        return value

class TweetSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source = "user.profile", read_only = True)
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields = ["user", 
                  "id", 
                  "content", 
                  "likes", 
                  "is_retweet", 
                  "parent",
                  "timestamp"]
        
    def get_likes(self, obj):
        return obj.likes.count()
    
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)
    
    def validate_action(self, value):
        value = value.lower().strip()
        if value in TWEET_ACTION_OPTIONS:
            return value
        else:
            raise serializers.ValidationError("action not valid")
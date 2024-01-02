from rest_framework import serializers
from .models import Profile


class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "location",
            "follower_count",
            "following_count",
            "is_following"
        ]

    def get_is_following(self, obj):
        context = self.context
        request = context.get("request")
        is_following = True if request.user in obj.followers.all() else False
        return is_following

    @staticmethod
    def get_first_name(obj):
        return obj.user.first_name

    @staticmethod
    def get_last_name(obj):
        return obj.user.last_name

    @staticmethod
    def get_username(obj):
        return obj.user.username

    @staticmethod
    def get_follower_count(obj):
        return obj.followers.count()

    @staticmethod
    def get_following_count(obj):
        return obj.user.following.count()

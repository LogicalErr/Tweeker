from rest_framework import serializers
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token


class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')

    is_following = serializers.SerializerMethodField(read_only=True)
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
        request = context.get("request") or None
        user = request.user or None
        is_following = True if user in obj.followers.all() else False
        return is_following

    @staticmethod
    def get_follower_count(obj):
        return obj.followers.count()

    @staticmethod
    def get_following_count(obj):
        return obj.user.following.count()


class EditProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "email",
            "bio",
            "location",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return super().update(instance, validated_data)

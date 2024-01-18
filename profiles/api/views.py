from profiles.models import Profile
from rest_framework.response import Response
from profiles.serializers import PublicProfileSerializer, EditProfileSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.core.cache import cache
from profiles import cache_keys


class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get(request):
        profile = Profile.objects.get(user=request.user)
        serializer = EditProfileSerializer(profile)
        
        return Response(serializer.data)
    
    @staticmethod
    def put(request):
        profile = Profile.objects.get(user=request.user)
        serializer = EditProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        

class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_profile_object(username):
        cache_key = cache_keys.WEB_PROFILE_DETAIL_CACHE_KEY.format(username=username)
        profile_obj = cache.get(cache_key)
        if not profile_obj:
            try:
                profile_obj = Profile.objects.get(user__username=username)
                cache.set(cache_key, profile_obj)
            except Profile.DoesNotExist:
                profile_obj = None
        return profile_obj

    def get(self, request, username):
        profile_obj = self.get_profile_object(username)
        if profile_obj is None:
            return Response({"detail": "The user profile you're looking for didn't found!"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, username):
        profile_obj = self.get_profile_object(username)
        if profile_obj is None:
            return Response({"detail": "The user profile you're looking for didn't found!"},
                            status=status.HTTP_404_NOT_FOUND)

        request_data = request.data or {}
        request_user = request.user
        action = request_data.get("action", None)
        if profile_obj.user != request_user:
            if action:
                if action.lower() == "follow":
                    profile_obj.followers.add(request_user.id)
                elif action.lower() == "unfollow":
                    profile_obj.followers.remove(request_user)
            else:
                return Response({"action": [
                    "This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

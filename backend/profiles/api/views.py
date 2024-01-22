from profiles.models import Profile
from rest_framework.response import Response
from profiles.serializers import PublicProfileSerializer, EditProfileSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.core.cache import cache
from profiles import cache_keys
from profiles.cache import ProfileDetailCache


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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get(request, username):
        profile_obj = ProfileDetailCache.get_profile(username)
        if profile_obj is None:
            try:
                profile_obj = Profile.objects.get(user__username=username)
                ProfileDetailCache.set_profile(username, profile_obj)
            except Profile.DoesNotExist:
                return Response({"detail": "User profile didn't found!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, username):
        # profile_obj = self.get_profile_object(username)
        profile_obj = ProfileDetailCache.get_profile(username)
        if profile_obj is None:
            try:
                profile_obj = Profile.objects.get(user__username=username)
                ProfileDetailCache.set_profile(username, profile_obj)
            except Profile.DoesNotExist:
                return Response({"detail": "User profile didn't found!"}, status=status.HTTP_404_NOT_FOUND)

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

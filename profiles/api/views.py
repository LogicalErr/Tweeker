from profiles.models import Profile
from rest_framework.response import Response
from profiles.serializers import PublicProfileSerializer, EditProfileSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


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
    def get(request, username):
        try:
            profile_obj = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({"detail": "The user profile you're looking for didn't found"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, username):
        try:
            profile_obj = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({"detail": "The user profile you're looking for didn't found"},
                            status=status.HTTP_404_NOT_FOUND)

        data = request.data or {}
        user = request.user
        action = data.get("action", None)
        if profile_obj.user != user:
            if action:
                if action.lower() == "follow":
                    profile_obj.followers.add(user.id)
                elif action.lower() == "unfollow":
                    profile_obj.followers.remove(user)
            else:
                return Response({"detail": "Action parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

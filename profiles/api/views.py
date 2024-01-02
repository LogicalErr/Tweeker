from profiles.models import Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from profiles.serializers import PublicProfileSerializer
from rest_framework import status


@api_view(["GET", "POST"])
def profile_detail_api_view(request, username, *args, **kwargs):
    try:
        profile_obj = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data or None

    if request.method == "POST":
        user = request.user
        action = data.get("action", None)
        if profile_obj.user != user:
            if action is not None:
                if action == "follow":
                    profile_obj.followers.add(user)
                elif action == "unfollow":
                    profile_obj.followers.remove(user)
    serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def user_follow_view(request, username, *args, **kwargs):
#     me = request.user
#     other_user_qs = User.objects.filter(username=username)
#     if me.username == username:
#         my_followers = me.profile.followers.all() 
#         return Response({"count": my_followers.count()}, status=200)
    
#     if not other_user_qs.exists():
#         return Response({}, status=400)
#     other = other_user_qs.first()
#     profile = other.profile
#     try:
#         data = request.data
#     except:
#         data = {}
#     action = data.get("action")
#     if action == "follow":
#         profile.followers.add(me)
#     elif action == "unfollow": 
#         profile.followers.remove(me)
#     else:
#         pass
#     if me in profile.followers.all():
#         profile.followers.remove(me)
#     else:
#         profile.followers.add(me)
#     data = PublicProfileSerializer(instance = profile, context={"request": request})
#     return Response(data.data, status=200)

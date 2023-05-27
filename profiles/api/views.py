from django.conf import settings
from ..models import Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def user_profile_detail_view(request, username, *args, **kwargs):
#     current_user = request.user
#     to_follow_user
#     return Response({}, status=400)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def user_follow_view(request, username, *args, **kwargs):
    me = request.user
    other_user_qs = User.objects.filter(username=username)
    if me.username == username:
        my_followers = me.profile.followers.all() 
        return Response({"count": my_followers.count()}, status=200)
    
    if not other_user_qs.exists():
        return Response({}, status=400)
    other = other_user_qs.first()
    profile = other.profile
    try:
        data = request.data
    except:
        data = {}
    action = data.get("action")
    if action == "follow":
        profile.followers.add(me)
    elif action == "unfollow": 
        profile.followers.remove(me)
    else:
        pass
    if me in profile.followers.all():
        profile.followers.remove(me)
    else:
        profile.followers.add(me)
    current_followers_qs = profile.followers.all() 
    return Response({"count": current_followers_qs.count()}, status=200)

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from itertools import chain


# Create your models here.
class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
class TweetQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact = username)
    
    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_user_id = []
        if profiles_exist:
            followed_user_id = user.following.values_list("user__id", flat=True)
        feed_tweets = self.filter(
                                            Q(user__id__in= followed_user_id) | 
                                            Q(user = user)
                                            ).distinct().order_by("-timestamp")
        other_tweets = Tweet.objects.exclude(
                                            Q(user__id__in= followed_user_id) | 
                                            Q(user = user)
                                            ).distinct().order_by("-timestamp")
        response_tweets = list(chain(feed_tweets, other_tweets)) # First you see tweets of users that you follow, and then you see other users' tweets 
        return response_tweets
class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetQuerySet(self.model, using=self._db)
    
    def feed(self, user):
        return self.get_queryset().feed(user)
class Tweet(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets") # one-to-many a user can have many tweets
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="tweet_user", blank=True, through=TweetLike)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = TweetManager()
    class Meta:
        ordering = ["-id"]
    
    @property
    def is_retweet(self):
        return self.parent != None    
        
    # def __str__(self):
    #     return self.content
    

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from itertools import chain


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class TweetQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)
    
    def feed(self, user):
        # profiles_exist = user.following.exists()
        # followed_user_ids = []
        # if profiles_exist:
        #     followed_user_ids = user.following.values_list("user__id", flat=True)
        followed_user_ids = user.following.values_list("user__id", flat=True)
        
        tweets_in_feed = Q(user__id__in=followed_user_ids) | Q(user=user)
        
        feed_tweets = self.filter(tweets_in_feed).distinct().order_by("-timestamp")
        other_tweets = Tweet.objects.exclude(tweets_in_feed).distinct().order_by("-timestamp")

        # First you see tweets of users that you follow, and then you see other users' tweets
        response_tweets = list(chain(feed_tweets, other_tweets))
        return response_tweets


class TweetManager(models.Manager):
    def get_queryset(self):
        return TweetQuerySet(self.model, using=self._db)
    
    def feed(self, user):
        return self.get_queryset().feed(user)


class Tweet(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")  # one user can have many tweets
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="tweet_user", blank=True, through=TweetLike)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = TweetManager()

    class Meta:
        ordering = ["-id"]
    
    @property
    def is_retweet(self):
        return self.parent is not None

    # def __str__(self):
    #    return self.content

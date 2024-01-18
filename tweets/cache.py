from django.core.cache import cache
from tweets import cache_keys


class TweetsListCache:
    cache_key = cache_keys.WEB_TWEETS_LIST_CACHE_KEY

    @staticmethod
    def get_tweets_list():
        tweets_list = cache.get(TweetsListCache.cache_key) or None
        return tweets_list

    @staticmethod
    def set_tweets_list(tweets):
        cache.set(TweetsListCache.cache_key, tweets)

    @staticmethod
    def delete_tweet_from_list(tweet):
        tweets_list = TweetsListCache.get_tweets_list()
        if tweets_list is not None:
            new_tweets_list = tweets_list.exclude(id=tweet.id)
            TweetsListCache.set_tweets_list(new_tweets_list)


class TweetDetailCache:
    cache_key = cache_keys.WEB_TWEET_DETAIL_CACHE_KEY

    @staticmethod
    def get_tweet(tweet_id):
        tweet = cache.get(TweetDetailCache.cache_key.format(tweet_id=tweet_id)) or None
        return tweet

    @staticmethod
    def set_tweet(tweet):
        cache.set(TweetDetailCache.cache_key.format(tweet_id=tweet.id), tweet)

    @staticmethod
    def delete_tweet(tweet):
        cache.delete(TweetDetailCache.cache_key.format(tweet_id=tweet.id))
        TweetsListCache.delete_tweet_from_list(tweet)

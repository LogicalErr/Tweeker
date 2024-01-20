from django.core.cache import cache
from profiles import cache_keys


class ProfileDetailCache:
    cache_key = cache_keys.WEB_PROFILE_DETAIL_CACHE_KEY

    @staticmethod
    def get_profile(username):
        profile = cache.get(ProfileDetailCache.cache_key.format(username=username)) or None
        return profile

    @staticmethod
    def set_profile(username, profile):
        cache.set(ProfileDetailCache.cache_key.format(username=username), profile)

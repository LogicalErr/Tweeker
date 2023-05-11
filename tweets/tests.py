from django.test import TestCase
from .models import Tweet
from django.contrib.auth.models import User
from rest_framework.test import APIClient
# Create your tests here.
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="abc", password="somepassword")
        Tweet.objects.create(content= "my 1st tweet", user= self.user)
        Tweet.objects.create(content= "my 2nd tweet", user= self.user)
        Tweet.objects.create(content= "my 3rd tweet", user= self.user)
        Tweet.objects.create(content= "my 4th tweet", user= self.user)
        
    def test_tweet_created(self):
        tweet = Tweet.objects.create(content= "my 5th tweet", user= self.user)
        self.assertEqual(tweet.id, 5)
        self.assertEqual(tweet.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="somepassword")
        return client
    
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        
    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 1)
        
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/tweets/action/", {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 0)
    
    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 2, "action": "retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertNotEqual(2, new_tweet_id)
        
    def test_action_create_api_view(self):
        request = {"content": "my tweek", }
        client = self.get_client()
        response = client.post("/api/tweets/create/", request)
        self.assertEqual(response.status_code, 201)
        
    def test_action_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)
        
    def test_action_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 204)
        # data = response.json()
        # _id = data.get("id")
        # self.assertEqual(_id, 1)
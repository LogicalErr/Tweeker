from django.db import models
from django.contrib.auth.models import User
import random


# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # one-to-many a user can have many tweets
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    
    class Meta:
        ordering = ["-id"]
    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 99999)
        }
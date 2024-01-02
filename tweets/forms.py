from django import forms
from tweets.models import Tweet
from django.conf import settings

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError(f"This tweet is more than {MAX_TWEET_LENGTH} characters")
        return content
    
    def serialize(self):
        return {
            "id": self.cleaned_data.get("id"),
            "content": self.cleaned_data.get("content"),
        }

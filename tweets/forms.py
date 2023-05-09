from django import forms
from .models import Tweet

MAX_TWEET_LENGTH = 280

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is more than {} characters".format(MAX_TWEET_LENGTH))
        return content
    
    def serialize(self):
        return{
            "id": self.cleaned_data.get("id"),
            "content": self.cleaned_data.get("content"),
            "id": self.cleaned_data.get("id"),
        }
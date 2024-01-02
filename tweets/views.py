from django.shortcuts import render


def home_view(request, *args, **kwargs):
    context = {
        "can_tweet": False
    }
    if request.user.is_authenticated:
        context["can_tweet"] = "true"
    return render(request, "tweets/list.html", context=context)
    # return render(request, "pages/feed.html")


# def tweets_list_view(request, *args, **kwargs):
#     return render(request, "tweets/list.html")


def tweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, "tweets/detail.html", context={"tweet_id": tweet_id})

import { BackendLookup } from "../lookup"

export function apiTweetCreate(newTweets, callback){
    BackendLookup("POST", "tweets/create/", callback, {content: newTweets})
}

export function apiTweetAction(tweetId, action, callback){
    let endpoint = "tweets/action/"
    const data = {id: tweetId, action: action}
    BackendLookup("POST", endpoint, callback, data)
}

export function apiTweetDetail(tweetId, callback) {
    BackendLookup("GET", `tweets/${tweetId}/`, callback)
}

export function apiTweetList(username, callback, nextUrl) {
    let endpoint = "tweets/"
    if (username != null){
        endpoint = `tweets/?username=${username}`
    }

    if (nextUrl !== null && nextUrl !== undefined){
        endpoint = nextUrl.replace("http://localhost:8000/api/v1/", "")
    }

    BackendLookup("GET", endpoint, callback)
}

export function apiTweetFeed(callback, nextUrl) {
    let endpoint = "tweets/feed/"

    if (nextUrl !== null && nextUrl !== undefined){
        endpoint = nextUrl.replace("http://localhost:8000/api/v1/", "")
    }
    BackendLookup("GET", endpoint, callback)
}

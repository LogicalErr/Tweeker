import { BackendLookup } from "../lookup"

export function apiTweetCreate(newTweets, callback){
    BackendLookup("POST", "tweets/create/", callback, {content: newTweets})
}

export function apiTweetAction(tweetId, action, callback){
    const data = {id: tweetId, action: action}
    BackendLookup("POST", "tweets/action/", callback, data)
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
        endpoint = nextUrl.replace("http://localhost:8000/api/", "")
    }
    BackendLookup("GET", endpoint, callback)
}
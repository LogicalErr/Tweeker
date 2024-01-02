import React, { useEffect, useState } from "react";
import { TweetsList } from "./list";
import { TweetCreate } from "./create";
import { apiTweetDetail } from "./lookup";
import { Tweet } from "./detail";
import { FeedList } from "./feed";

export function TweetsComponent(props){
    const [newTweets, setNewTweets] = useState([])
    const canTweet = props.canTweet === 'true'

    const handleNewTweet = (newTweet) => {
        let tempNewTweets = [...newTweets]
        tempNewTweets.unshift(newTweet)
        setNewTweets(tempNewTweets)
    }

    return <div className={props.className}>
                {canTweet && <TweetCreate didTweet={handleNewTweet} className="col-lg-8 col-md-8 col-sm-8 mx-auto pt-4 mb-3" />}
                <TweetsList newTweets={newTweets} didRetweet={handleNewTweet} canTweet={props.canTweet}/>
            </div>
}

export function FeedComponent(props){
    const [newTweets, setNewTweets] = useState([])
    const canTweet = props.canTweet === "false" ? false : true
    const handleNewTweet = (newTweet) => {
        let tempNewTweet = [...newTweets]
        tempNewTweet.unshift(newTweet)
        setNewTweets(newTweet)
    }
    return <div className={props.className}>
                {canTweet === true && <TweetCreate didTweet={handleNewTweet} className="col-lg-8 mx-auto pt-4 mb-3" />}
                <FeedList newTweets={newTweets} {...props}/>
            </div>
}

export function TweetDetailComponent(props){    
    const {tweetId} = props
    const [didLookup, setDidLookup] = useState(false)
    const [tweet, setTweet] = useState(null)

    const className = props.className ? props.className : "my-5 col-lg-10 mx-auto col-md-8 py-5 border border-secondary rounded-5 text-white"

    const handleBackendLookup = (response, status) => {
        if (status === 200){
            setTweet(response)
        } else {
            alert(`There was an error during showing the tweet! status code: ${status}`)
        }
    }
    useEffect(() => {
        if (didLookup === false){
            apiTweetDetail(tweetId, handleBackendLookup)
            setDidLookup(true)
        }
    }, [tweetId, didLookup, setDidLookup])
    console.log('here')
    return tweet ? <Tweet tweet={tweet} className={className} /> : null 
}

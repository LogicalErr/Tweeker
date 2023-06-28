import React, { useEffect, useState } from "react";
import { TweetsList } from "./list";
import { TweetCreate } from "./create";
import { apiTweetDetail } from "./lookup";
import { Tweet } from "./detail";
import { FeedList } from "./feed";

export function TweetsComponent(props){
    const [newTweets, setNewTweets] = useState([])
    const canTweet = props.canTweet === "false" ? false : true
    const handleNewTweet = (newTweet) => {
        let tempNewTweet = [...newTweets]
        tempNewTweet.unshift(newTweet)
        setNewTweets(newTweet)
    }
    return <div className={props.className}>
                {canTweet === true && <TweetCreate didTweet={handleNewTweet} className="col-lg-8 mx-auto pt-4 mb-3" />}
                <TweetsList newTweets={newTweets} {...props}/>
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
    console.log(props.className)
    const [didLookup, setDidLookup] = useState(false)
    const [tweet, setTweet] = useState(null)
    const handleBackendLookup = (response, status) => {
        if (status === 200){
            setTweet(response)
        } else {
            alert("There was an error finding the tweet.")
        }
    }
    useEffect(() => {
        if (didLookup === false){
            apiTweetDetail(tweetId, handleBackendLookup)
            setDidLookup(true)
        }
    }, [tweetId, didLookup, setDidLookup])
    return tweet === null ? null : <Tweet tweet={tweet} className={props.className} /> 
}


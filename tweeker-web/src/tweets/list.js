import React, {useEffect, useState} from "react";
import { apiTweetList } from "./lookup";
import { Tweet } from "./detail";

export function TweetsList(props) {
    const [tweetsInit, setTweetsInit] = useState([])
    const [tweets, setTweets] = useState([])
    const [nextUrl, setNextUrl] = useState(null)
    const [tweetsDidSet, setTweetsDidSet] = useState(false)
    useEffect(() => {
        const final = [...props.newTweets].concat(tweetsInit)
        if (final.length !== tweets.length){
            setTweets(final)
        }
    }, [props.newTweets, tweets, tweetsInit])

    useEffect(() =>{
        if (tweetsDidSet === false ){
            const handleTweetListLookup = (response, status)  => {
                if (status === 200){
                    setNextUrl(response.next)
                    setTweetsInit(response.results)  
                    setTweetsDidSet(true)    
                } else {
                    console.log(response, status)
                    alert("There was an error.")
                }
            }   
            apiTweetList(props.username, handleTweetListLookup)
        }
        
    }, [tweetsInit, tweetsDidSet, props.username, setTweetsDidSet]) 
    const handleDidRetweet = (newTweet) => {
        let updateTweetsInit = [...tweetsInit]
        updateTweetsInit.unshift(newTweet)
        setTweetsInit(updateTweetsInit)
        let updateFinalTweets = [...tweets]
        updateFinalTweets.unshift(tweets)
        setTweets(updateFinalTweets)
    }
    const handleLoadNext = (event) =>{
        event.preventDefault()
        if (nextUrl !== null) {
            const handleLoadNextResponse = (response, status) => {
                if (status === 200){
                    setNextUrl(response.next)
                    const newTweets = [...tweets].concat(response.results)
                    setTweetsInit(newTweets)
                    setTweets(newTweets)
                } else {
                    alert("There was an error.")
                }
            }
            apiTweetList(props.username, handleLoadNextResponse, nextUrl)
        }
    }

    return <React.Fragment>
        <div className="col-8 mx-auto">
            {tweets.map((item, index) => {
            return <Tweet 
                tweet={item} 
                didRetweet={handleDidRetweet}
                className="py-5 border-secondary border-bottom text-white" 
                key={`${index}-{item.id}`}/>
                })}
            { nextUrl !== null && <button onClick={handleLoadNext} className="btn btn-outline-primary text-white mb-5 mt-3" >Show more</button>}
        </div> 
    </React.Fragment>
}
import React, {useEffect, useState} from "react";
import { apiTweetList } from "./lookup";
import { Tweet } from "./detail";

export function TweetsList(props) {
    const [tweetsInit, setTweetsInit] = useState([])
    const [tweets, setTweets] = useState([])
    const [nextUrl, setNextUrl] = useState(null)
    const [tweetsDidSet, setTweetsDidSet] = useState(false)
    const {username} = props
    const {didRetweet} = props
    
    useEffect(() => {
        const newTweetsList = [...props.newTweets].concat(tweetsInit)
        if (newTweetsList.length !== tweets.length){
            setTweets(newTweetsList)
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
                    alert(`There was an error during fetching user tweets! status code: ${status}`)
                }
            }   
            apiTweetList(username, handleTweetListLookup)
        }
    
    }, [tweetsInit, tweetsDidSet, username, setTweetsDidSet]) 

    const handleDidRetweet = (newTweet) => {
        if (didRetweet !== null && didRetweet !== undefined){
            didRetweet(newTweet)            
        }
        // let addNewTweet = [...tweetsInit]
        // addNewTweet.unshift(newTweet)

        // setTweetsInit(addNewTweet)
        // setTweets(addNewTweet)

        // let updateFinalTweets = [...tweets]
        // updateFinalTweets.unshift(tweets)
        // setTweets(updateFinalTweets)
    }

    const handleLoadNext = (event) =>{
        event.preventDefault()

        if (nextUrl) {
            const handleLoadNextPageOfTweets = (response, status) => {
                if (status === 200){
                    const moreLoadedTweets = [...tweets].concat(response.results)
                    setNextUrl(response.next)
                    setTweetsInit(moreLoadedTweets)
                    setTweets(moreLoadedTweets)
                } else {
                    alert(`There was an error during loading more tweets! status code ${status}`)
                }
            }
            apiTweetList(username, handleLoadNextPageOfTweets, nextUrl)
        }
    }

    return <React.Fragment>
            <div className="col-lg-9 col-md-10 col-sm-11 mx-auto">
                {tweets.map((item, index) => {
                return <Tweet 
                    tweet={item} 
                    didRetweet={handleDidRetweet}
                    className="py-3 border-secondary border-top text-white" 
                    key={`${index}-{item.id}`}/>
                    })}
                { nextUrl && <button onClick={handleLoadNext} className="btn btn-outline-primary text-white mb-5 mt-3" >Show more</button>}
            </div> 
        </React.Fragment>
}

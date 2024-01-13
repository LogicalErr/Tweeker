import React from 'react'
import { useState, useEffect, useContext } from 'react'
import axios from 'axios';
import Tweet from '../components/Tweet';
import CreateNewTweet from '../components/CreateNewTweet';
import AuthContext from '../context/AuthContext';


export default function TweetsList(props) {
    const { user } = useContext(AuthContext)

    const [tweets, setTweets] = useState([])
    const [nextUrl, setNextUrl] = useState(null)
    const [tweetsDidSet, setTweetsDidSet] = useState(false)

    const {username, disableSendTweet} = props

    useEffect(() =>{
        if (tweetsDidSet === false ){
                const tweetsUrl = username
                    ? `http://localhost:8000/api/v1/tweets/?username=${username}`
                    : "http://localhost:8000/api/v1/tweets/"
                
                axios.get(tweetsUrl)
                .then(response => {
                    const status = response.status
                    const data = response.data
                    if (status === 200){
                        setNextUrl(data.next)
                        setTweets(data.results)
                        setTweetsDidSet(true)    
                    } else {
                        console.log(data)
                        alert(`Something went wrong! status code: ${status}`)
                    }
                })
                .catch(error =>{
                    const data = error.response.data
                    const status = error.response.status
                    console.log(status, data)
                    alert(`${data.detail}! status code: ${status}`)
                })
        }
    }, [tweetsDidSet, username, setTweetsDidSet])

    const handleNewTweet = (newTweet) => {
        let newTweets = [...tweets]
        newTweets.unshift(newTweet)
        setTweets(newTweets)
    }
    
    const handleLoadNext = (event) =>{
        event.preventDefault()
        if (nextUrl) {
            axios.get(nextUrl)
            .then((response) => {
                const status = response.status
                const data = response.data
                if (status === 200){
                    const moreLoadedTweets = [...tweets].concat(data.results)
                    setNextUrl(data.next)
                    setTweets(moreLoadedTweets)
                } else {
                    alert(`There was an error during loading more tweets! status code ${status}`)
                }
            })
        }
    }

    return (
        <div>
            {user && !disableSendTweet &&
                <CreateNewTweet className="mb-5" didTweet={handleNewTweet}>
                </CreateNewTweet>
            }
        <div className="col-lg-8 col-md-10 col-sm-8 mx-auto">
            {tweets.map((item, index) => {
            return <Tweet
                tweet={item}
                didRetweet={handleNewTweet}
                className="py-4 border-secondary border-bottom text-light"
                key={`${index}-{item.id}`}/>
                })}
            { nextUrl && <button onClick={handleLoadNext} className="btn btn-outline-primary text-light mb-5 m-3" >Show more</button>}
        </div>
        </div>
    )
}
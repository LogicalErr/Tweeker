import axios from 'axios'
import React from 'react'
import { useState, useEffect } from "react"
import { useParams } from 'react-router-dom'
import Tweet from '../components/Tweet'

const TweetDetail = () => {
    const { tweetId } = useParams()
    const [didLookup, setDidLookup] = useState(false)
    const [tweet, setTweet] = useState(null)


    const defaultClassName = "col-lg-8 col-md-8 p-4 mx-auto border border-secondary rounded-5 text-white"

    const handleTweet = (response, status) => {
        if (status === 200){
            setTweet(response)
        } else {
            alert(`There was an error during showing the tweet! status code: ${status}`)
        }
    }

    useEffect(() => {
        if (didLookup === false){
            axios.get(`http://localhost:8000/api/v1/tweets/${tweetId}/`)
            .then(response => {
                handleTweet(response.data, response.status)
                setDidLookup(true)
            })
            .catch(error => {
                console.log(error.response.data, error.response.status)
            })
        }

    }, [tweetId, didLookup, setDidLookup])

    return (
        tweet ? <Tweet tweet={tweet} className={defaultClassName} hideViewLink/> :
        <div className='text-light text-center'>
            The tweet your looking for doesn't found!
        </div>
    )
}

export default TweetDetail
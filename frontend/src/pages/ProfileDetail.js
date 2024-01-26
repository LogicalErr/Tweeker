import React from 'react'
import { useParams } from 'react-router-dom'
import { useState, useEffect, useContext} from "react"
import axios from 'axios'
import TweetsList from './TweetsList'
import UserPicture from '../components/UserPicture'
import UserDisplay from '../components/UserDisplay'
import AuthContext from '../context/AuthContext'
import DisplayCount from '../components/DisplayCount'

function ProfileBadge(props) {
    const { user } = useContext(AuthContext)
    const { authTokens } = useContext(AuthContext)
    const { profile, didFollowToggle } = props
    const currentVerb = profile.is_following ? "Unfollow" : "Follow"

    const handleFollowToggle = (event) => {
        event.preventDefault()
        if (didFollowToggle) {
          didFollowToggle(currentVerb, authTokens)
        }
    }

    return(
        <div className='text-white m-5 p-5 border border-secondary rounded-5'>
            <UserPicture user={profile} hideLink/>
            <span><UserDisplay user={profile} includeFullName includeUsername hideLink/></span>
            <div className='mx-5 my-3 px-5'>
                <p>
                    <span><DisplayCount>{profile.follower_count}</DisplayCount> {profile.follower_count <= 1 ? "follower" : "followers"}</span>
                    <span className='mx-3'>|</span>
                    <span><DisplayCount>{profile.following_count}</DisplayCount> following</span>
                </p>
              {profile.location ? <p>Location: {profile.location}</p> : null}
              {profile.bio ? <p>Bio: {profile.bio}</p> : null}
            </div>
            {user && user.user_id !== profile.id && <button className='btn btn-primary' onClick={handleFollowToggle}>{currentVerb}</button>}
        </div>
    )

}


export default function Profile() {
  const { username } = useParams()

  const [didLookup, setDidLookup] = useState(false)
  const [profile, setProfile] = useState(null)


  useEffect(() => {
      if (didLookup === false){

          axios.get(`http://localhost:8000/api/v1/profiles/${username}`)
          .then(response => {
              if (response.status === 200) {
                  setProfile(response.data)
                  setDidLookup(true)
              } else {
                  alert(`${response.data.detail}! status code: ${response.status}`)
              }
          })
          .catch(error => {
              console.log(error.response)
              alert(`Something went wrong! status code: ${error.response.status}`)
          })
      }
  }, [username, didLookup, setDidLookup])

  const handleNewFollow = (actionVerb, authTokens) => {
      const data = {action: `${actionVerb && actionVerb}`.toLowerCase()}
      axios.post(`http://localhost:8000/api/v1/profiles/${username}/follow/`, data,
          {
              "headers": {
                  "Content-Type": "application/json",
                  "Authorization": `Bearer ${authTokens.access}`
              }
          })
      .then(response => {
        const data = response.data
        const status = response.status
        console.log(data)
        
        if (status === 200) {
          setProfile(data)
        } else {
          alert(`There was an error during the action! status code: ${status}`)
        }
      })
  }

  return (
    <div>
      {profile ?
      <div>
        <ProfileBadge profile={profile} didFollowToggle={handleNewFollow}/>
        <TweetsList username={username} disableSendTweet />
      </div>
      : <div className='text-light text-center'>The user profile you're looking for doesn't found!</div>}
    </div>
  )
}

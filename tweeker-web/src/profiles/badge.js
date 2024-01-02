import React, {useEffect, useState} from 'react'
import { apiProfileDetail, apiProfileFollowToggle } from './lookup'
import { UserDisplay, UserPicture } from './components'
import { DisplayCount } from './utils'
import { TweetsList } from '../tweets/list'

function ProfileBadge(props) {
    const {user, didFollowToggle, profileLoading} = props
    let currentVerb = (user && user.is_following) ? "Unfollow" : "Follow"
    
    currentVerb = profileLoading ? "Loading..." : currentVerb

    const handleFollowToggle = (event) => {
        event.preventDefault()
        if (didFollowToggle && !profileLoading){
            didFollowToggle(currentVerb)
        }
    }

    return user ? 
                <div className='text-white m-5 p-5 border border-secondary rounded-5'>
                    <UserPicture user={user} hideLink/>
                    <span><UserDisplay user={user} includeFullName includeUsername hideLink/></span>
                    <div className='mx-5 my-3 px-5'>
                        <p> 
                            <span><DisplayCount>{user.follower_count}</DisplayCount> {user.follower_count <= 1 ? "follower" : "followers"}</span>   
                            <span className='mx-3'>|</span>
                            <span><DisplayCount>{user.following_count}</DisplayCount> following</span>
                        </p>
                        {user.location ? <p>Location: {user.location}</p> : null}
                        {user.bio ? <p>Bio: {user.bio}</p> : null}
                    </div>
                    <button className='btn btn-primary' onClick={handleFollowToggle}>{currentVerb}</button>
                </div> 
        : null
}

export function ProfileBadgeComponent(props) {
    const {username} = props
    
    // lookup
    const [didLookup, setDidLookup] = useState(false)
    const [profile, setProfile] = useState(null)
    const [profileLoading, setProfileLoading] = useState(false)

    const handleProfileDetailLookup = (response, status) => {
        if (status === 200) {
            setProfile(response)
        }
        else {
            alert(`there was an error durring loading the profile! status code: ${status}`)
        }
    }

    useEffect(() => {
        if (didLookup === false){
            apiProfileDetail(username, handleProfileDetailLookup)
            setDidLookup(true)
        }
    }, [username, didLookup, setDidLookup])

    const handleNewFollow = (actionVerb) => {
        apiProfileFollowToggle(username, actionVerb, (response, status) => {  
            if (status === 200) {
                setProfile(response)
            }
            else {
                alert(`There was an error during the action! status code: ${status}`)
            }
            setProfileLoading(false)
        })
        setProfileLoading(true)
    }
    return didLookup === false ? "Loading..." : 
        <div>
                {profile ? <ProfileBadge user={profile} didFollowToggle={handleNewFollow} profileLoading={profileLoading}/>: null}
                <TweetsList newTweets={[]} username={props.username}/>
        </div>
}

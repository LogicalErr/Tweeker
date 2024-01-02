import React, { useState } from "react";
import { ActionBtn } from "./buttons";
import { 
    UserDisplay, 
    UserPicture 
} from "../profiles";

function ParentTweet(props){
    const {tweet} = props
    // let className = isRetweet === true ? `${className} p-2 my-2 col-6` : className
    return (tweet.parent ? <Tweet isRetweet hideActionButtons={true} className='p-2 my-2 col-6' tweet={tweet.parent}/> : null)
}

export function Tweet(props){
    const {tweet, didRetweet, hideActionButtons} = props
    const [actionTweet, setActionTweet] = useState(tweet ? tweet : null)
    
    let className = props.className ? props.className : "col-lg-8 col-md-6 mx-auto text-light"

    
    const path = window.location.pathname
    const match = path.match(/(?<tweetId>\d+)/)
    const urlTweetId = match ? match.groups.tweetId : null
    
    const isDetail = `${tweet.id}` === `${urlTweetId}`
    
    const handleLink = (event) => {
        event.preventDefault()
        window.location.href = `/${tweet.id}`
    }

    const handlePerformAction = (response, status) => {
        if (status === 200){
            setActionTweet(response)
        }else if (status === 201) {
            if (didRetweet){
                didRetweet(response)
            }
        }
    }

    return <div className={className}>
                {/* {isRetweet && <div className="mb-2"> 
                                            <span className="small text-secondary">Retweeted <UserDisplay user={retweeter.user}/></span>
                                        </div>} */}
                <div className="d-flex">
                    <div>
                        <UserPicture user={tweet.author} />
                    </div>
                    <div className="col-11">
                        <div>
                            <p className="d-flex">
                                {tweet.is_retweet ? 
                                    <React.Fragment>
                                        <UserDisplay includeFullName user={tweet.author}/>
                                            <span className="small text-secondary mx-1">Retweeted</span>
                                    </React.Fragment> :
                                    <React.Fragment>
                                        <UserDisplay includeFullName includeUsername user={tweet.author}/>
                                    </React.Fragment>
                                }
                            </p>
                            <p>{tweet.content}</p>
                            <ParentTweet tweet={tweet}/>
                        </div>
                        <div className='btn btn-group px-0'>
                            {(actionTweet && hideActionButtons !== true) && 
                                <React.Fragment>
                                    <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:"like", display:"Likes"}} />
                                    <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:"unlike", display:"Unlike"}} />
                                    <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} className="btn btn-outline-success text-white" action={{type:"retweet", display:"Retweet"}} />
                                </React.Fragment>
                            }
                                {isDetail === true ? null : <button className="btn btn-outline-primary text-white btn-sm" onClick={handleLink}>View</button>}
                        </div>
                    </div>
                </div>
            </div>
}
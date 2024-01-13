import React, { useState, useContext } from "react";
import UserPicture from "./UserPicture"
import UserDisplay from "./UserDisplay"
import ActionBtn from "./ActionBtn";
import AuthContext from "../context/AuthContext";

function ParentTweet(props){
  const {tweet} = props
  return (tweet.parent ? <Tweet isRetweet hideActionButtons={true} className='p-2 my-2 col-6' tweet={tweet.parent}/> : null)
}

export default function Tweet(props) {
  const { user } = useContext(AuthContext)

  const {tweet, didRetweet, hideActionButtons, hideViewLink} = props
  const [actionTweet, setActionTweet] = useState(tweet ? tweet : null)
  const className = props.className ? props.className : "col-lg-8 col-md-6 mx-auto text-light"

  const handlePerformAction = (response, status) => {
    if (status === 200){
        setActionTweet(response)
    }else if (status === 201) {
      if (didRetweet !== null && didRetweet !== undefined){
        didRetweet(response)
      }
    }
  }

  const handleViewLink = (e) => {
    e.preventDefault()
    window.location.href = `/tweets/${tweet.id}`
  }

  return (
    <div className={className}>
      <div className="d-flex">
        <div><UserPicture user={tweet.author} /></div>
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
          <div className='btn btn-group'>
              {(user && actionTweet && hideActionButtons !== true) &&
                  <React.Fragment>
                      <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:"like", display:"Likes"}} />
                      <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:"unlike", display:"Unlike"}} />
                      <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} className="btn btn-outline-success text-white" action={{type:"retweet", display:"Retweet"}} />
                  </React.Fragment>
              }
              {hideViewLink ? null : <button className="btn btn-outline-primary text-white btn-sm" onClick={handleViewLink}>View</button>}
          </div>
        </div>
      </div>
    </div>
  )
}



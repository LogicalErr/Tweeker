import React from 'react'
import UserLink from './UserLink'
export default function UserDisplay(props) {
  const {user, includeFullName, includeUsername, hideLink} = props

  const fullNameDisplay = includeFullName === true ? `${user.first_name} ${user.last_name}` : null
  const usernameDisplay = includeUsername === true ?  `@${user.username}` : null
  
  if (user !== undefined){
    return (
      <React.Fragment>
        <span className="mx-1 pointer">{hideLink === true ? fullNameDisplay : <UserLink username={user.username}>{user ? fullNameDisplay : ""}</UserLink>}</span>
        <span className="text-secondary pointer">{hideLink === true ? usernameDisplay : <UserLink username={user.username}>{user ? usernameDisplay : ""}</UserLink>}</span>                        
      </React.Fragment>
    )
  }
}

import React from "react";

export function UserLink(props) {
    const {username} = props
    const handleUserLink = (event) => {
        window.location.href = `/profiles/${username}`
    }
    return <span className="pointer" onClick={handleUserLink}>
                {props.children}
            </span>
}

export function UserDisplay(props){
    const {user, includeFullName, includeUsername, hideLink} = props
    
    const fullNameDisplay = includeFullName === true ? `${user.first_name} ${user.last_name}` : null
    const usernameDisplay = includeUsername === true ?  `@${user.username}` : null
    
    if (user !== undefined){
        return <React.Fragment>
                        <span className="mx-1 pointer">{hideLink === true ? fullNameDisplay : <UserLink username={user.username}>{user ? fullNameDisplay : ""}</UserLink>}</span>
                        <span className="text-secondary pointer">{hideLink === true ? usernameDisplay : <UserLink username={user.username}>{user ? usernameDisplay : ""}</UserLink>}</span>                        
                </React.Fragment>
    }
}

export function UserPicture(props){
    const {user, hideLink} = props
    const userIdSpan = <span className="mx-2 py-2 px-3 pointer rounded-circle bg-primary text-light">{user.username[0]}</span>
    return hideLink ? userIdSpan : <UserLink username={user.username}>{userIdSpan}</UserLink>
}

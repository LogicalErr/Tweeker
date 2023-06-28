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
    const {user, includeFullName, hideLink} = props
    const nameDisplay = includeFullName === true ? `${user.first_name} ${user.last_name} ` : null
    if (user !== undefined){
        return <React.Fragment>
                    {nameDisplay}
                    <span className="text-secondary">{hideLink === true ? `@${user.username}` : <UserLink username={user.username}>{user ? `@${user.username}` : ""}</UserLink>}</span>                        
                </React.Fragment>
    }
}

export function UserPicture(props){
    const {user, hideLink} = props
    const userIdSpan = <span className="mx-2 py-2 px-3 rounded-circle bg-primary text-light">{user.username[0]}</span>

    return hideLink === true ? userIdSpan : <UserLink username={user.username}>{userIdSpan}</UserLink>
}
import React from 'react'

export default function UserLink(props) {
    const {username} = props
    const handleUserLink = (e) => {
        window.location.href = `/profiles/${username}`
    }
    return (
        <span className="pointer" onClick={handleUserLink}>
            {props.children}
        </span>
    )
}

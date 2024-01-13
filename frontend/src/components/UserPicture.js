import React from 'react'
import UserLink from "./UserLink"

export default function UserPicture(props) {
  const {user, hideLink} = props
  const userIdSpan = <span className="mx-2 py-2 px-3 pointer rounded-circle bg-primary text-light">{user.username[0]}</span>
  return hideLink ? userIdSpan : <UserLink username={user.username}>{userIdSpan}</UserLink>
}

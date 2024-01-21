import { useContext } from 'react'
import React from 'react'
import { Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'

const Header = () => {
  const {user} = useContext(AuthContext)

  const className = 'navbar navbar-expand-lg border-bottom mb-5 rounded-2 text-white mb-2'
  const linkClassName = 'link-light mx-2 px-4 py-2 border-secondary rounded text-muted bg-secondary text-decoration-none'

  return (
    <nav className={className}>
      <Link className='text-light mx-5 pb-2 text-decoration-none display-6' to="#">Tweeker</Link>
      <Link className={linkClassName} to="/">Home</Link>
      <span className='text-secondary'>|</span>
      {user ? 
        <div className='auth-user'>
            <Link className={linkClassName} to="/profiles/edit">Profile</Link>
            <span className='text-secondary'>|</span>
            <Link className={linkClassName} to="/logout">Logout</Link>
        </div> :
        <Link className={linkClassName} to="/login">Login</Link>}
    </nav>
  )
}

export default Header
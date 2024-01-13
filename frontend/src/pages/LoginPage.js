import React from 'react'
import { useContext } from 'react'
import AuthContext from '../context/AuthContext'
import { Link } from 'react-router-dom'


export default function LoginPage() {
  const { loginUser } = useContext(AuthContext)

  const handleSubmitForm = (e) =>{
    e.preventDefault()
    loginUser(e.target.username.value, e.target.password.value)
  }

  return (
    <div className='px-5 mx-5  text-light item-justify-center content-justify-center'>
      <div className='form-header'>
        <h3 className='text-light text-center bg-inline-secondary border-bottom border-secondary border-2 rounded-5 m-3 p-3'>Login</h3>
      </div>
      <form className='col-lg-4 offset-lg-4 px-5 pt-5 pb-1 mt-5 border border-2 border-secondary rounded-5' onSubmit={handleSubmitForm} >

        <div className='row my-3 px-4'>
          <label htmlFor="username" className="form-label">Username:</label>
          <input type="text" name='username' className='border rounded form-control'/>
        </div>

        <div className='row my-3 px-4'>
          <label htmlFor="password" className="form-label">Password:</label>
          <input type="password" name='password' className='border rounded form-control'/>
        </div>

        <div className='row'>
          <div className='col'>
            <button type='submit' className='mx-2 px-4 btn btn btn-success btn-block text-light' >Login</button>
          </div>
        </div>

        <div className='row'>
          <div className='col text-center mt-4'>
            <Link className='text-light text-decoration-none' to="/signup">don't have an account? Register now.</Link>
          </div>
        </div>

      </form>
    </div>
  )
}

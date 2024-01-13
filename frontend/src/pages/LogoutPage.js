import React from 'react'
import { useContext } from 'react'
import AuthContext from '../context/AuthContext'

export default function LogoutPage() {
    const { logoutUser } = useContext(AuthContext)

    return (
        <div className='px-5 mx-5 text-light'>
            <div className='form-header'>
                <h3 className='text-light text-center border-bottom border-secondary border-2 rounded-5 m-3 p-3'>Logout</h3>
            </div>
            <form className='col-lg-4 offset-lg-4 px-5 mt-5 rounded-5 text-center' onSubmit={logoutUser}>
                <button type='submit' className='btn btn btn-success text-light' >Are you sure you want to log out?</button>
            </form>
        </div>
    )
}

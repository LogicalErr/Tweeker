import axios from 'axios'
import React from 'react'
import { useState, useEffect, useContext } from 'react'
import AuthContext from '../context/AuthContext'

export default function ProfileEdit() {

    const { authTokens } = useContext(AuthContext)

    const [profileDidSet, setProfileDidSet] = useState(false)
    const [profile, setProfile] = useState(null)

    useEffect(() => {
        if (profileDidSet === false) {
            axios.get(`http://localhost:8000/api/v1/profiles/edit/`, {
                'headers':{
                    'Content-Type':'application/json',
                    'Authorization':'Bearer ' + String(authTokens.access)
                }
            })
            .then(response => {
                const data = response.data
                const status = response.status
                if (status === 200) {
                    setProfile(data)
                }
            })
            .catch(error => {
                const response = error.response
                console.log(response)
                alert(`${response.data.content}! status code: ${response.status}`)
            })
            setProfileDidSet(true)
        }
    }, [profileDidSet, authTokens])


    const handleSubmitForm = (e) => {
        e.preventDefault()
        const body = JSON.stringify({
            "first_name": e.target.first_name.value,
            "last_name": e.target.last_name.value,
            "location": e.target.location.value,
            "email": e.target.email.value,
            "bio": e.target.bio.value,
        })
        console.log(body)
        alert("profile updated")
        // axios.put(`http://localhost:8000/api/v1/profiles/edit/`, body, {
        //         'headers':{
        //             'Content-Type':'application/json',
        //             'Authorization':'Bearer ' + String(authTokens.access)
        //         }
        //     })
        //     .then(response => {
        //         const data = response.data
        //         const status = response.status
        //         console.log(data, status)
        //         if (status === 200) {
        //             setProfile(data)
        //         }
        //     })
        //     .catch(error => {
        //         const response = error.response
        //         console.log(response)
        //         alert(`${response.data.content}! status code: ${response.status}`)
        //     })
    }

    return (
        <div className='mx-5 text-light'>
            <div className='form-header'>
                <h3 className='text-center border-bottom border-secondary border-2 rounded-5 m-3 p-3'>Edit Profile</h3>
            </div>

            {profile ?
            <form onSubmit={handleSubmitForm} className='col-lg-8 offset-lg-2 p-5 border border-2 border-secondary rounded-5' >
                <div className='row'>
                    <div className='mb-3 col-lg-6'>
                        <label htmlFor="first_name" className="form-label">First name:</label>
                        <input type="text" name='first_name' defaultValue={profile.first_name} className='m-2 border rounded form-control'/>
                    </div>

                    <div className='mb-3 col-lg-6'>
                        <label htmlFor="last_name" className="form-label">Last name:</label>
                        <input type='text' name='last_name' defaultValue={profile.last_name} className='m-2 border rounded form-control'></input>
                    </div>
                </div>

                <div className='row'>
                    <div className='mb-3 col-lg-6'>
                        <label htmlFor="email" className="form-label col-form-label">Email:</label>
                        <input type='text' name='email' defaultValue={profile.email} className='m-2 border rounded form-control'></input>
                    </div>
                </div>

                <div className='row'>
                    <div className='mb-3 col-lg-12'>
                        <label htmlFor="location" className="form-label">Location:</label>
                        <input type='text' name='location' defaultValue={profile.location} className='m-2 border rounded form-control'></input>
                    </div>
                </div>

                <div className='row'>
                    <div className='mb-3 col-lg-12'>
                        <label htmlFor="bio" className="form-label">Bio:</label>
                        <textarea name='bio' defaultValue={profile.bio} className='m-2 border rounded form-control'></textarea>
                    </div>
                </div>
                <div className='row'>
                    <div className='col'>
                        <button type='submit' className='mx-2 px-4 btn btn btn-success text-light'>Save</button>
                    </div>
                </div>
            </form> :
            <div className='text-center p-5'>Loading your profile data...</div>
            }
        </div>
    )
}

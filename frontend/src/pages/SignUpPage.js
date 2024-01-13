import React from 'react'
import { useState, useContext } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import axios from "axios";
import authContext from "../context/AuthContext";

const SignUpPage = () => {
    const navigate = useNavigate()
    const [username, setUsername] = useState()
    const [email, setEmail] = useState()
    const [password1, setPassword1] = useState()
    const [password2, setPassword2] = useState()

    const {loginUser} = useContext(authContext)
    // const {name} = useContext(AuthContext)

    // console.log(loginUser)
    const handleChange = (event) => {
        const {name, value} = event.target
        switch (name){
            case 'username':
                setUsername(value)
                break
            case 'email':
                setEmail(value)
                break
            case 'password1':
                setPassword1(value)
                break
            case 'password2':
                setPassword2(value)
                break
            default:
                break
        }
    }

    const handleSubmitForm = (event) => {
        event.preventDefault()
        if (password1 !== password2){
            alert("Password and confirm password values doesn't match!")
        } else {
            const data = JSON.stringify({email:email, username:username, password:password1})
            axios.post("http://localhost:8000/auth/users/", data, {
                "headers": {
                    "Content-Type": "application/json"
                }
            })
                .then(response => {
                    console.log(response)
                    if (response.status === 201) {
                        alert("your account successfully created")
                        loginUser(username, password1)
                        navigate("/")
                    }
                })
                .catch(error => {
                    if (error.response.status === 400){
                        alert(`${error.response.data.password}`)
                    } else {
                        console.log(error.response)
                        alert(`Something went wrong during creating your account! status code: ${error.response.status}`)
                    }
                })
        }
    }

    return (
        <div className='px-5 mx-5  text-light item-justify-center content-justify-center'>

            <div className='form-header'>
                <h3 className='text-light text-center bg-inline-secondary border-bottom border-secondary border-2 rounded-5 m-3 p-3'>Signup</h3>
            </div>

            <form className='col-lg-4 offset-lg-4 px-5 pt-5 pb-1 mt-5 border border-2 border-secondary rounded-5' onChange={handleChange} onSubmit={handleSubmitForm}>
    
            <div className='row my-3 px-4'>
                <label htmlFor="username" className="form-label">Username:</label>
                <input type="text" name='username' className='border rounded form-control'/>
            </div>

            <div className='row my-3 px-4'>
                <label htmlFor="email" className="form-label">Email:</label>
                <input type="email" name='email' className='border rounded form-control'/>
            </div>
    
            <div className='row my-3 px-4'>
                <label htmlFor="password1" className="form-label">Password:</label>
                <input type="password" name='password1' className='border rounded form-control'/>
            </div>
    
            <div className='row my-3 px-4'>
                <label htmlFor="password2" className="form-label">Confirm password:</label>
                <input type="password" name='password2' className='border rounded form-control'/>
            </div>

            <div className='row'>
                <div className='col'>
                <button type='submit' className='mx-2 px-4 btn btn btn-success btn-block text-light'>Signup</button>
                </div>
            </div>
    
            <div className='row'>
                <div className='col text-center mt-4'>
                <Link className='text-light text-decoration-none' to="/login">Do you have an account? Login now.</Link>
                </div>
            </div>
    
            </form>
        </div>
    )
  }

export default SignUpPage
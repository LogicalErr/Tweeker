import { createContext, useEffect, useState } from "react";
import React from 'react'
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom"

const AuthContext = createContext()

export default AuthContext

export const AuthProvider = ({children}) => {
    const [authTokens, setAuthTokens] = useState(() => JSON.parse(localStorage.getItem("authTokens")) || null )
    const [user, setUser] = useState(() => authTokens ? jwtDecode(authTokens.access) : null)
    const [isLoading, setIsLoading] = useState(true)

    const navigate = useNavigate()

    const loginUser = (username, password) => {
        const body = JSON.stringify({'username':username, 'password':password})
        axios.post('http://localhost:8000/auth/jwt/create', body, {
            headers:{
                'Content-Type':'application/json',
            },
        })
        .then(response => {
            const data = response.data
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))
            navigate('/')
            return data
        })
        .catch(error => {
            const status = error.response.status
            if (status === 401){
                alert('Wrong username or password! Try again.')
            } else {
                alert(`Something went wrong during login you in. Status code: ${status}`)
            }
        })
    }

    const logoutUser = () => {
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem('authTokens')
        navigate('/')
    }

    const updateToken = () => {
        console.log("Update token called")
        if (authTokens){
            const body = JSON.stringify({'refresh':authTokens.refresh})
            axios.post('http://localhost:8000/auth/jwt/refresh/', body, {
                headers:{
                    'Content-Type':'application/json',
                },
            })
            .then(response => {
                const data = response.data
                const status = response.status
                if (status === 200) {
                    localStorage.setItem('authTokens', JSON.stringify(data))
                    setAuthTokens(data)
                    setUser(jwtDecode(data.access))
                    return data
                }
            })
            .catch(error => {
                const status = error.response.status
                if (status === 401){
                    console.log('Token is invalid or expired.')
                    logoutUser()
                } else {
                    console.log(`Something went wrong during updating token. Status code: ${status}`)
                    logoutUser()
                }
                logoutUser()
            })
        }

        if(isLoading){
            setIsLoading(false)
        }
    }


    useEffect(() => {
        if (isLoading){
            updateToken()
        }
        const fiveMinutes = 1000 * 60 * 4.9
        const interval = setInterval(() => {
            if (authTokens) {
                updateToken()
            }
        }, fiveMinutes)
        return () => clearInterval(interval)
    }, [authTokens, isLoading])

    const contextData = {
        authTokens:authTokens,
        user:user,
        loginUser:loginUser,
        logoutUser:logoutUser
    }

    return (
        <AuthContext.Provider value={contextData}>
            {isLoading ? null : children}
        </AuthContext.Provider>
    )
}
import React, { useContext } from 'react'
import axios from 'axios'
import AuthContext from '../context/AuthContext'

export default function ActionBtns(props) {
    const { authTokens } = useContext(AuthContext)

    const {tweet, action, didPerformAction} = props
    const likes = tweet.likes ? tweet.likes : 0
    const className = props.className ? props.className : "btn btn-outline-primary btn-sm text-white"
    const actionDisplay = action.display ? action.display : "Acion"
    
    const handleActionBackendEvent = (response, status) => {
        if ((status === 200 || status === 201) && didPerformAction) {
            didPerformAction(response, status)
        }
        else {
            console.log(`something wend wrong with the action! status code ${status}`)
        }

    }

    const handleClick = (event) =>{
        event.preventDefault()
        const body = {id: tweet.id, action: action.type}
        axios.post('http://localhost:8000/api/v1/tweets/action/', body, {
            'headers':{
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })
        .then(response => {
            handleActionBackendEvent(response.data, response.status)
        })
    }

    const btnLabel = action.type === "like" ? `${likes} ${actionDisplay}` : actionDisplay 
    
    return <button className={className} onClick={handleClick}>{btnLabel}</button>
}

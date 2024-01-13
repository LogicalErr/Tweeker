import React, { useContext } from 'react'
import axios from "axios"
import AuthContext from '../context/AuthContext'

export default function CreateNewTweet(props) {
    const { authTokens } = useContext(AuthContext)
    const textAreaRef = React.createRef()
    const {didTweet} = props

    const handleDidTweet = (response, status) => {
        if (status === 201){
            didTweet(response)
        } else {
            console.log(response.content)
            alert(`${response.content}! status code: ${status}`)
        }
    }

    const handleSubmitForm = (event) => {
        event.preventDefault()

        const tweetContent = textAreaRef.current.value
        const body = JSON.stringify({content:tweetContent})

        axios.post("http://localhost:8000/api/v1/tweets/create/", body, {
            'headers':{
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })
        .then(response => {
            const status = response.status
            const data = response.data
            handleDidTweet(data, status)
        })
        .catch(error => {
            const response = error.response
            console.log(response)
            if (response.status === 400){
                alert(response.data.content[0])
            } else {
                alert(`Something went wrong during post your tweet! status code ${response.status}`)
            }
        })

        textAreaRef.current.value = ""
    }
    
    return (
        <div className={props.className}>
            <form className='col-lg-8 offset-lg-2' onSubmit={handleSubmitForm}>
                <div className='row mb-3'>
                    <textarea ref={textAreaRef} required name='tweet' className='rounded text-justify px-4 py-2 form-control' placeholder="What's happening...?"/>
                </div>
                <div className='tow'>
                    <div className='col'>
                        <button className='btn btn-outline-primary text-light'>Tweet</button>
                    </div>
                </div>
            </form>

        </div>
    )
}

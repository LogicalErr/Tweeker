import React, { useContext } from "react";
import authContext from "../context/AuthContext";

export default function MyProfile() {
    const { user } = useContext(authContext)
    return (
        <div className="text-light text-center">{ user.username }</div>
    )
}
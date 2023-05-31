import { BackendLookup } from "../lookup"

export function apiProfileDetail(username, callback) {
    BackendLookup("GET", `profiles/${username}`, callback)
}

export function apiProfileFollowToggle(username, action, callback) {
    const data = {action: `${action && action}`.toLowerCase()}
    BackendLookup("POST", `profiles/${username}/follow`, callback, data)
}
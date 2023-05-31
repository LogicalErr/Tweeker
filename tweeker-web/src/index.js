import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { TweetsComponent, TweetDetailComponent, FeedComponent } from './tweets';
import { ProfileBadgeComponent } from './profiles';

const appEl = document.getElementById('root')
if (appEl){
  const root = ReactDOM.createRoot(appEl)
  root.render(<App />)
}

const tweetsEl = document.getElementById('tweeker')
const e = React.createElement
if (tweetsEl){
  const root = ReactDOM.createRoot(tweetsEl)
  root.render(
    e(TweetsComponent, tweetsEl.dataset)
    )
}

const tweetFeedEl = document.getElementById('tweeker-feed')
if (tweetFeedEl){
  const root = ReactDOM.createRoot(tweetFeedEl)
  root.render(
    e(FeedComponent, tweetFeedEl.dataset)
    )
}


const tweetDetailEl = document.querySelectorAll(".tweeker-detail")
tweetDetailEl.forEach(container => {
  const root = ReactDOM.createRoot(container)
  root.render(
    e(TweetDetailComponent, container.dataset))
})

const userProfileBadgeEl = document.querySelectorAll(".tweeker-profile-badge")
userProfileBadgeEl.forEach(container => {
  const root = ReactDOM.createRoot(container)
  root.render(
    e(ProfileBadgeComponent, container.dataset))
})


// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
  // <React.StrictMode>
    // <App />
  // </React.StrictMode>
// );

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

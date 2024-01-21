import './App.css';
import { 
  BrowserRouter as Router, 
  Route, 
  Routes
} from "react-router-dom"
import LoginPage from "./pages/LoginPage"
import TweetsList from './pages/TweetsList';
import TweetDetail from './pages/TweetDetail';
import ProfileDetail from './pages/ProfileDetail';
import Header from "./components/Header"
import React from 'react';
import ProfileEdit from './pages/ProfileEdit';
import SignUpPage from './pages/SignUpPage';
import { AuthProvider } from './context/AuthContext';
import LogoutPage from './pages/LogoutPage';
import PrivateRoute from './utils/PrivateRoute'


function App() {
  return (
    <div className="App bg-dark">
      <Router>
        <AuthProvider>
          <Header />
          <Routes>
            <Route path='/' Component={TweetsList} exact></Route>
            <Route path='/tweets/:tweetId' Component={TweetDetail}></Route>
            <Route path='/profiles/edit' element={<PrivateRoute />}>
              <Route path='/profiles/edit' Component={ProfileEdit}></Route>
            </Route>
            <Route path='/profiles/:username' Component={ProfileDetail}></Route>

            <Route Component={LoginPage} path='/login' />

            <Route path='/logout' element={<PrivateRoute />}>
              <Route Component={LogoutPage} path='/logout' />
            </Route>

            <Route Component={SignUpPage} path='/signup' />
          </Routes>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
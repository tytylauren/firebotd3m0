import React, { useState } from 'react';
import Login from './Login';
import './App.css';
import DroneLauncher from './LaunchDrone';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');

  const handleLogin = (username) => {
    setIsLoggedIn(true);
    setUsername(username);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername('');
  };

  return (
    <div className="App moving-background">
      {isLoggedIn ? (
        <>
          <div className="dropdown">
            <button className="dropbtn">{username}</button>
            <div className="dropdown-content">
              <button onClick={handleLogout}>Logout</button>
            </div>
          </div>
          <div className="grid-container">
	    <DroneLauncher />
	    <button className="rounded-button">Button 2</button>
            <button className="rounded-button">Button 3</button>
            <button className="rounded-button">Button 4</button>
            <button className="rounded-button">Button 5</button>
            <button className="rounded-button">Button 6</button>
          </div>
        </>
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;

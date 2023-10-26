import React, { useState } from 'react';
import axios from 'axios';

function DroneLauncher() {
    const [message, setMessage] = useState('');

    const launchDrone = () => {
        axios.post('http://127.0.0.1:8000/launch_simulation/')
            .then(response => {
                if (response.data.status === "Simulation started") {
                    setMessage('DRONE LAUNCHED');
                } else {
                    setMessage('Failed to launch drone.');
                }
            })
            .catch(error => {
                setMessage('Error: ' + error.message);
            });
    };

    return (
        <div>
            <button onClick={launchDrone}>Launch Drone</button>
            <p>{message}</p>
        </div>
    );
}

export default DroneLauncher;

!#/bin/bash

# Install required npm packages
npm install axios react-router-dom

echo "import logo from './logo.svg';
import './App.css';
import React from 'react';
import VideoFeed from './VideoFeed';
import React, { useState, useEffect } from 'react';
import axios from 'axios';


function App() {

const [droneInfo, setDroneInfo] = useState(null);
const [coordinates, setCoordinates] = useState(null);

  const connectToDrone = async () => {
    const droneData = await axios.get('/api/drone_info');
    setDroneInfo(droneData.data);

    const coordinateData = await axios.get('/api/live_coordinates');
    setCoordinates(coordinateData.data);
  };



const startMission = async () => {
  try {
    const response = await axios.post('/api/start_mission/');
    console.log("Start Mission:", response.data);
  } catch (error) {
    console.error("Error starting mission:", error);
  }
}

const pauseMission = async () => {
  try {
    const response = await axios.post('/api/pause_mission/');
    console.log("Pause Mission:", response.data);
  } catch (error) {
    console.error("Error pausing mission:", error);
  }
}

const resumeMission = async () => {
  try {
    const response = await axios.post('/api/resume_mission/');
    console.log("Resume Mission:", response.data);
  } catch (error) {
    console.error("Error resuming mission:", error);
  }
}

const returnToBase = async () => {
  try {
    const response = await axios.post('/api/return_to_base/');
    console.log("Return to Base:", response.data);
  } catch (error) {
    console.error("Error returning to base:", error);
  }
}

 useEffect(() => {
    if (droneInfo) {
      const intervalId = setInterval(async () => {
        const coordinateData = await axios.get('/api/live_coordinates');
        setCoordinates(coordinateData.data);
      }, 5000);

      return () => clearInterval(intervalId);
    }
  }, [droneInfo]);

  return (
    <div className="App">
      <VideoFeed />
      <button onClick={connectToDrone}>Connect to Drone</button>
      {droneInfo && <div>Drone Info: {JSON.stringify(droneInfo)}</div>}
      {coordinates && <div>Coordinates: {JSON.stringify(coordinates)}</div>}
      <button onClick={startMission}>Start Mission</button>
      <button onClick={pauseMission}>Pause Mission</button>
      <button onClick={resumeMission}>Resume Mission</button>
      <button onClick={returnToBase}>Return to Base</button>
    </div>
  );
 }
  
export default App;" >> fbl_react_demo/src/App.js

echo "import React from 'react';

const VideoFeed = () => {
  return (
    <div>
      <h1>Video Feed from Gazebo</h1>
      <video src="http://localhost:8080/stream?topic=/camera/image_raw" type="video/mp4" controls>
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default VideoFeed;" >> fbl_react_demo/src/VideoFeed.js




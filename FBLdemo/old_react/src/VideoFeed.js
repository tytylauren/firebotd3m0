import React from 'react';

const VideoFeed = () => {
  return (
    <div>
      <h1>Video Feed from Gazebo</h1>
      <video src=http://localhost:8080/stream?topic=/camera/image_raw type=video/mp4 controls>
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default VideoFeed;

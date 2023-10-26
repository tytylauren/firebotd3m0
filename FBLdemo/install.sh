#!/bin/bash

# Navigate to the project directory
cd fbl_backend

# Create a virtual environment named 'venv'
sudo python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Update pip to the latest version
sudo pip install --upgrade pip
# Install Python dependencies
echo "Installing Python dependencies..."
sudo pip install -r requirements.txt

# Check if installation was successful
if [ $? -ne 0 ]; then
  echo "Failed to install Python dependencies."
  exit 1
fi


# Install QGroundControl

sudo usermod -a -G dialout $USER
sudo apt-get remove modemmanager -y
sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl -y
sudo apt install libqt5gui5 -y
sudo apt install libfuse2 -y
wget https://s3-us-west-2.amazonaws.com/qgroundcontrol/latest/QGroundControl.AppImage
chmod +x ./QGroundControl.AppImage


# Ubuntu Universe
sudo apt install software-properties-common
sudo add-apt-repository universe

# ROS Keys
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
# Install PX4
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
            
sudo ./PX4-Autopilot/Tools/setup/ubuntu.sh --no-nuttx

# Install ROS 2
sudo apt install ros-iron-desktop
sudo apt install ros-iron-ros-base
source /opt/ros/iron/setup.bash

# Install JavaScript dependencies
echo "Installing JavaScript dependencies..."
cd ..
cd fbl_frontend && npm install
npm install axios
# Check if installation was successful
if [ $? -ne 0 ]; then
  echo "Failed to install JavaScript dependencies."
  exit 1
fi

echo "Dependencies installed successfully."











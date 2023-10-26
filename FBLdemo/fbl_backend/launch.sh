#!/bin/bash

cd PX4-Autopilot
HEADLESS=1 make px4_sitl gz_x500_vision && python3 ../mavlink.py


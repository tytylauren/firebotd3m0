#!/bin/bash

cd PX4-Autopilot
make distclean
HEADLESS=1 make px4_sitl gz_x500_vision 


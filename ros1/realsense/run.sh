#!/bin/bash
source /catkin_ws/devel/setup.bash && roslaunch realsense2_camera rs_camera.launch enable_gyro:=true enable_accel:=true unite_imu_method:=linear_interpolation enable_depth:=false color_width:=640 color_height:=480 color_fps:=30

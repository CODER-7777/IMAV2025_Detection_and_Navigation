#!/bin/bash
roslaunch realsense2_camera rs_camera.launch enable_accel:=true enable_gyro:=true unite_imu_method:=linear_interpolation enable_color:=false enable_depth:=false gyro_fps:=400 accel_fps:=250

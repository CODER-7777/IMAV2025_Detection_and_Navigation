#!/bin/bash
ros2 launch realsense2_camera rs_launch.py enable_gyro:=true enable_accel:=true enable_infra1:=true enable_infra2:=true unite_imu_method:=2 infra_fps:=30 gyro_fps:=400 accel_fps:=250 infra_width:=640 infra_height:=480

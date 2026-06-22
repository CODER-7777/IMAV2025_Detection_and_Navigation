FROM docker.io/ros:humble
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y tmux neovim
RUN apt-get install -y ros-humble-realsense2-camera

# Zenoh DDS
RUN apt-get install -y ros-${ROS_DISTRO}-rmw-zenoh-cpp
ENV RMW_IMPLEMENTATION=rmw_zenoh_cpp
ENV ROS_DOMAIN_ID=0

CMD ["tmux"]

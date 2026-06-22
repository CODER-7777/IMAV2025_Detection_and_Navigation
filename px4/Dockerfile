FROM docker.io/ros:humble
# PX4-Autopilot Setup
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y curl lsb-release gnupg git
RUN git clone https://github.com/PX4/PX4-Autopilot.git --recursive
RUN apt-get install -y wget sudo
WORKDIR /PX4-Autopilot
RUN ./Tools/setup/ubuntu.sh
RUN apt-get install -y tmux ripgrep fd-find

# Loading Custom World
RUN apt-get install -y ros-${ROS_DISTRO}-ros-gzharmonic-bridge\
  ros-${ROS_DISTRO}-ros-gzharmonic-image ros-${ROS_DISTRO}-ros-gzharmonic-sim\
  ros-${ROS_DISTRO}-foxglove-bridge
RUN sudo apt-get install -y ros-humble-mavros-msgs
COPY px4_custom_env/models/blender_env /PX4-Autopilot/Tools/simulation/gz/models/blender_env
RUN rm /PX4-Autopilot/Tools/simulation/gz/worlds/default.sdf
COPY default.sdf /PX4-Autopilot/Tools/simulation/gz/worlds/default.sdf

# Zenoh DDS
RUN apt-get install -y ros-${ROS_DISTRO}-rmw-zenoh-cpp
ENV ROS_DOMAIN_ID=0
ENV RMW_IMPLEMENTATION=rmw_zenoh_cpp

RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc
COPY ros_gz.yaml .
COPY run.sh .
RUN chmod +x run.sh
CMD [ "./run.sh" ]

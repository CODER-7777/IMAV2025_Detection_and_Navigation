FROM ros:humble
RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y ros-${ROS_DISTRO}-mavros ros-${ROS_DISTRO}-mavros-extras tmux
RUN wget https://raw.githubusercontent.com/mavlink/mavros/ros2/mavros/scripts/install_geographiclib_datasets.sh
RUN chmod +x install_geographiclib_datasets.sh
RUN ./install_geographiclib_datasets.sh
# Zenoh DDS
RUN apt-get install -y ros-${ROS_DISTRO}-rmw-zenoh-cpp
ENV RMW_IMPLEMENTATION=rmw_zenoh_cpp
ENV ROS_DOMAIN_ID=0

CMD ["ros2","launch","mavros","px4.launch","fcu_url:=udp://:14551@"]

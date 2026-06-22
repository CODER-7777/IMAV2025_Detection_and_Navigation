FROM ros:noetic
SHELL ["/usr/bin/bash","-c"]
RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y neovim ripgrep tmux wget


# librealsnese
RUN wget https://github.com/IntelRealSense/librealsense/archive/refs/tags/v2.50.0.tar.gz
RUN mkdir -p /librealsense
RUN tar xvf v2.50.0.tar.gz --directory=/
RUN mkdir -p /librealsense-2.50.0/build
WORKDIR /librealsense-2.50.0/build
RUN apt-get update && apt-get install -y git wget cmake build-essential\
            libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev at\
            libssl-dev libusb-1.0-0-dev libudev-dev pkg-config libgtk-3-dev
RUN cmake ../ -DFORCE_RSUSB_BACKEND=true -DCMAKE_BUILD_TYPE=release -DBUILD_EXAMPLES=true -DBUILD_GRAPHICAL_EXAMPLES=true
RUN make -j$(nproc) && make install

# Realsense ROS
RUN apt-get update && apt-get install -y ros-${ROS_DISTRO}-ddynamic-reconfigure python3-catkin-tools ros-$ROS_DISTRO-foxglove-bridge
WORKDIR /catkin_ws/src
RUN git clone --branch ros1-legacy https://github.com/IntelRealSense/realsense-ros.git

# Kalibr and allan_variance_ros
ENV DEBIAN_FRONTEND = noninteractive apt-get install keyboard-configuration
RUN apt-get update && apt-get install -y python3-catkin-tools python3-osrf-pycommon
RUN apt-get update && apt-get install -y \
    git wget autoconf automake\
    libeigen3-dev libboost-all-dev libsuitesparse-dev \
    doxygen libopencv-dev libpoco-dev \
    libtbb-dev libblas-dev liblapack-dev libv4l-dev
RUN apt-get update && apt-get install -y python3-dev python3-scipy \
    python3-matplotlib ipython3 python3-wxgtk4.0 \
    python3-tk python3-igraph python3-pyx python3-numpy
RUN git clone https://github.com/ethz-asl/kalibr.git
RUN git clone https://github.com/ori-drs/allan_variance_ros.git



# ROVIO
RUN apt-get update && apt-get install -y libeigen3-dev libyaml-cpp-dev ros-${ROS_DISTRO}-hector-trajectory-server
RUN git clone https://github.com/ethz-asl/kindr.git
# RUN git clone --recursive https://github.com/ethz-asl/rovio.git # Original
RUN git clone --recursive https://github.com/AerialRobotics-IITK/rovio.git

RUN apt-get update && apt-get install -y ros-${ROS_DISTRO}-cv-bridge \
                ros-${ROS_DISTRO}-tf2 ros-${ROS_DISTRO}-image-transport \
                ros-${ROS_DISTRO}-tf2-geometry-msgs ros-${ROS_DISTRO}-eigenpy ros-${ROS_DISTRO}-diagnostic-updater
WORKDIR /catkin_ws
RUN catkin init
RUN catkin config --extend /opt/ros/${ROS_DISTRO}
RUN catkin config --merge-devel
RUN catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release
RUN catkin build -DCMAKE_BUILD_TYPE=Release -j$(nproc)
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc
RUN echo "source /catkin_ws/devel/setup.bash" >> ~/.bashrc
CMD ["tmux"]

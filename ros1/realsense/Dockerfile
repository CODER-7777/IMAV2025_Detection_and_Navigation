FROM ros:noetic
SHELL ["/usr/bin/bash","-c"]
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y tmux wget curl
RUN wget https://github.com/IntelRealSense/librealsense/archive/refs/tags/v2.50.0.tar.gz
RUN mkdir -p /librealsense
RUN tar xvf v2.50.0.tar.gz --directory=/
RUN mkdir -p /librealsense-2.50.0/build
WORKDIR /librealsense-2.50.0/build
RUN apt-get update && apt-get install -y git wget cmake build-essential\
            libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev at\
            libssl-dev libusb-1.0-0-dev libudev-dev pkg-config libgtk-3-dev
RUN cmake ../ -DFORCE_RSUSB_BACKEND=true -DCMAKE_BUILD_TYPE=release -DBUILD_EXAMPLES=true -DBUILD_GRAPHICAL_EXAMPLES=true
RUN make -j && make install
RUN apt-get update && apt-get install -y ros-${ROS_DISTRO}-ddynamic-reconfigure python3-catkin-tools ros-$ROS_DISTRO-foxglove-bridge
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws/src
RUN git clone --branch ros1-legacy https://github.com/IntelRealSense/realsense-ros.git
RUN . /opt/ros/noetic/setup.sh && catkin_init_workspace
WORKDIR /catkin_ws
RUN rosdep install --from-paths src -y --ignore-src --include-eol-distros
RUN . /opt/ros/noetic/setup.sh && catkin_make clean
RUN . /opt/ros/noetic/setup.sh && catkin_make -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release
RUN . /opt/ros/noetic/setup.sh && catkin_make install
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
RUN echo "source /catkin_ws/devel/setup.bash" >> ~/.bashrc
COPY run.sh .
RUN chmod +x run.sh
COPY record.sh .
RUN chmod +x record.sh
CMD [ 'tmux' ]

#!/usr/bin/bash
source /opt/ros/humble/setup.bash
SESSION="IMAV_SIM"

tmux new-session -d -s $SESSION
tmux send-keys -t $SESSION:0 'make px4_sitl gz_x500_depth' C-m

tmux split-window -h -t $SESSION
tmux send-keys -t $SESSION:0.1 'ros2 launch foxglove_bridge foxglove_bridge_launch.xml' C-m

tmux split-window -v -t $SESSION
tmux send-keys -t $SESSION:0.2 'ros2 run rmw_zenoh_cpp rmw_zenohd' C-m

tmux split-window -h -t $SESSION
tmux send-keys -t $SESSION:0.3 'ros2 run ros_gz_bridge parameter_bridge --ros-args -p config_file:=ros_gz.yaml' C-m

tmux attach-session -t $SESSION

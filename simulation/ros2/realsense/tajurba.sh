docker run --privileged \
  --device=/dev/bus/usb \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --env="TERM=xterm-256color" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --volume="/dev:/dev" \
  --volume="/var/run/dbus/:/var/run/dbus/:z" \
  --volume="$(pwd)/data":/data \
  -it --rm --net=host realsense tmux

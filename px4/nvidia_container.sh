#!/usr/bin/bash
sudo docker run -it \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --env="NVIDIA_VISIBLE_DEVICES=all" \
  --env="NVIDIA_DRIVER_CAPABILITIES=all" \
  --env="TERM=xterm-256color" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --volume="/dev:/dev" \
  --volume="/var/run/dbus/:/var/run/dbus/:z" \
  --volume ~/.ssh/ssh_auth_sock:/ssh-agent \
  --env SSH_AUTH_SOCK=/ssh-agent \
  --net=host \
  --runtime=nvidia \
  --gpus all \
  --name imavsim-env \
  imav-sim

docker rm mavros-env
docker build -t mavros .
docker run -it -e DISPLAY --net=host --name mavros-env mavros
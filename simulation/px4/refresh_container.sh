docker rm imavsim-env
docker build -t imav-sim .
docker run -it -e DISPLAY --net=host --name imavsim-env imav-sim

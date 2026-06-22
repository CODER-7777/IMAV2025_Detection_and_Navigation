# Imav2025

## Simulation Setup
1. Add the following to your '.profile' file
```bash
xhost +local:docker>/dev/null
```
1. Run docker container(first time) by running the following command
```bash
docker compose up -d --build
```
## Note: In QGC Application Settings -> comm link -> Add new communication link (UDP with port 14552)


### Intel/AMD
1. Run the following
```bash
docker compose start
```

### Nvidia
1. Instiall Nvidia Official Drivers
2. Setup Nvidia Container Toolkit from [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
3. Run the following
```bash
docker compose -f nvidia.yaml up -d --build
```
## ROS Workspace Setup
1. Install Dev Containers in VSCode
2. Select Reopen folder in container
3. Run the following command if src folder is not present
```bash
mkdir task1 task2 task3 task4 interfaces navigation
```

# IMAV2025_Detection_and_Navigation

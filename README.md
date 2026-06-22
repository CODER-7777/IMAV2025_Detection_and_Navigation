# IMAV2025_Detection_and_Navigation

**IMAV 2025 Competition | Task 1: Autonomous MAV Gate Detection & Tunnel Navigation**

## Overview

This repository contains the perception pipeline and Software-In-The-Loop (SITL) simulation stack developed for the International Micro Air Vehicle (IMAV) 2025 competition.

### Project Highlights
- **Objective:** Architect a **YOLO perception pipeline** to detect color-coded gates for autonomous MAV tunnel navigation.
- **Approach:** 
  - Fine-tuned a **YOLO** model via **Roboflow** to classify Wide/Medium/Small gates for optimal alignment precision.
  - Built a **Blender** 3D environment mirroring the indoor arena and imported it into **Gazebo** for simulation.
  - Validated the perception stack via SITL using a containerized **ROS2, Docker, MAVROS, & ArduPilot** stack.
- **Results:** Enabled the MAV to autonomously thread continuous 2-meter multi-gate corridors with high reliability.

## Repository Structure

The repository is organized into two primary components:

1. **`simulation/`**: Contains the complete Dockerized infrastructure required to run the physics simulation and flight controller.
2. **`task1/`**: Contains the ROS 2 packages and Python scripts responsible for the computer vision pipeline and drone control logic.

---

## 1. Simulation Setup (`/simulation`)

The simulation environment is built upon a multi-container Docker architecture, isolating the flight controller, routing, and ROS bridges. 

### Architecture Components
- **PX4 Autopilot**: Runs the flight control software in SITL mode, integrated with Gazebo for accurate physical simulation.
- **MAVLink Router**: Acts as a central hub to route MAVLink telemetry between the simulated drone, ROS 2, and external ground control stations (e.g., QGroundControl).
- **MAVROS (ROS 2)**: Bridges the MAVLink protocol to standard ROS 2 topics, allowing the custom control nodes to interface with the drone.

### Deployment Instructions

#### Prerequisites
Ensure Docker and Docker Compose are installed on your system. For optimal performance with Gazebo, a dedicated NVIDIA GPU and the NVIDIA Container Toolkit are highly recommended.

#### Running the Simulation
1. Allow local X11 connections for the Gazebo GUI:
   ```bash
   xhost +local:docker > /dev/null
   ```

2. Navigate to the simulation directory:
   ```bash
   cd simulation
   ```

3. Launch the container stack based on your hardware:
   - **For Intel/AMD Graphics:**
     ```bash
     docker compose up -d --build
     ```
   - **For NVIDIA Graphics (Hardware Accelerated):**
     ```bash
     docker compose -f nvidia.yaml up -d --build
     ```

4. Connect QGroundControl (optional):
   - In QGroundControl Application Settings -> Comm Links -> Add new communication link (UDP with port `14552`).

---

## 2. Gate Detection & Control Pipeline (`/task1`)

The core mission logic relies on a YOLO-based perception pipeline designed to classify and navigate through Wide, Medium, and Small color-coded gates.

### System Workflow
1. **Perception**: A YOLO object detection model, fine-tuned using Roboflow, processes incoming camera feeds to identify gate dimensions and color profiles.
2. **Environment Modeling**: A custom 3D environment mirroring the indoor arena was designed in Blender and imported into the Gazebo simulation.
3. **Control Execution**: Custom ROS 2 nodes process the bounding box coordinates to compute optimal alignment vectors, allowing the MAV to autonomously thread continuous 2-meter multi-gate corridors.

### Development Workflow
The recommended development environment utilizes VSCode Dev Containers attached directly to the running ROS 2 instance.
1. Install the "Dev Containers" extension in VSCode.
2. Select "Reopen in Container" to attach to the pre-configured ROS 2 development environment.
3. Source the ROS 2 workspace located within the `task1/ros2_ws` directory before executing the control scripts.

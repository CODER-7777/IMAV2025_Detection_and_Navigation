import asyncio
from mavsdk import System
from mavsdk.offboard import VelocityBodyYawspeed

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point


class MidpointSubscriber(Node):
    def __init__(self):
        super().__init__('midpoint_listener')
        self.midpoint = None
        self.detect_after_takeoff = False

        self.subscription = self.create_subscription(
            Point,
            '/rectangle_midpoint',
            self.midpoint_callback,
            10
        )

    def midpoint_callback(self, msg):
        if self.detect_after_takeoff:
            self.midpoint = (msg.x, msg.y)
            self.get_logger().info(f"[✓] Midpoint detected: x={msg.x:.1f}, y={msg.y:.1f}")
        else:
            self.get_logger().info("[✗] Midpoint received but ignored (too early)")


async def spin_ros_node(node):
    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=0.1)
        await asyncio.sleep(0.01)


async def move_drone(drone, node):
    print("Connecting and arming...")
    await drone.action.arm()

    print("Setting takeoff altitude to 1.5 meters...")
    await drone.action.set_takeoff_altitude(1.5)

    print("Taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(15)

    print("Sending initial setpoints...")
    for _ in range(10):
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0)
        )
        await asyncio.sleep(0.1)

    print("Starting Offboard mode...")
    try:
        await drone.offboard.start()
    except Exception as e:
        print(f"Failed to start offboard mode: {e}")
        await drone.action.land()
        return
    await asyncio.sleep(3)

    node.detect_after_takeoff = True
    print("Now detecting rectangles...")

    # Phase 1: Move right until detection
    print("Searching: Moving right slowly to find the rectangle...")
    while node.midpoint is None:
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.05, 0.0, 0.0)  # Move right slowly
        )
        await asyncio.sleep(0.1)

    print("[✓] Rectangle detected. Aligning...")

    # Phase 2: Align before moving forward
    target_center_x = 640
    pixel_tolerance = 30

    while abs(node.midpoint[0] - target_center_x) > pixel_tolerance:
        direction = 0.1 if node.midpoint[0] > target_center_x else -0.1
        print(f"Aligning... midpoint_x = {node.midpoint[0]:.1f}, direction = {direction}")
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.1, direction, 0.0, 0.0)
        )
        await asyncio.sleep(0.1)

    print("[✓] Aligned. Now moving forward with continuous alignment...")

    # Phase 3: Move forward while continuously aligning
    for _ in range(350):  # ~10 seconds
        if node.midpoint is not None:
            x_offset = node.midpoint[0] - target_center_x
            if abs(x_offset) > pixel_tolerance:
                direction = 0.1 if x_offset > 0 else -0.1
            else:
                direction = 0.0
        else:
            direction = 0.0  # If no detection, don’t adjust

        print(f"Moving forward... x_offset={x_offset:.1f}, lateral={direction}")
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.1, direction, 0.0, 0.0)
        )
        await asyncio.sleep(0.1)

    print("Hovering...")
    for _ in range(20):  # ~2 seconds hover
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0)
        )
        await asyncio.sleep(0.1)

    print("Stopping Offboard mode...")
    try:
        await drone.offboard.stop()
    except Exception as e:
        print(f"Failed to stop offboard mode: {e}")

    print("Landing...")
    await drone.action.land()


async def run():
    rclpy.init()
    node = MidpointSubscriber()
    ros_task = asyncio.create_task(spin_ros_node(node))

    drone = System()
    await drone.connect(system_address="udp://:14552")

    await move_drone(drone, node)

    node.destroy_node()
    rclpy.shutdown()
    await ros_task


if __name__ == "__main__":
    asyncio.run(run())

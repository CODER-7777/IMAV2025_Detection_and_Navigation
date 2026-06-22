import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np


class VisionNavigation(Node):
    def __init__(self):
        super().__init__('vision_navigation')

        # Subscribers and Publishers
        self.subscription = self.create_subscription(
            Image,
            '/front_cam/image',
            self.image_callback,
            10
        )
        self.publisher = self.create_publisher(Point, '/rectangle_midpoint', 10)

        # Tools
        self.bridge = CvBridge()
        self.get_logger().info("VisionNavigation node started. Subscribed to /front_cam/image.")

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Detect rectangles and get the midpoint of the target
            midpoint = self.detect_rectangle(cv_image)
            if midpoint:
                pt_msg = Point()
                pt_msg.x = float(midpoint[0])
                pt_msg.y = float(midpoint[1])
                pt_msg.z = 0.0
                self.publisher.publish(pt_msg)
                self.get_logger().info(f"Published TARGET midpoint: {midpoint}")

            # Display image with overlays
            cv2.imshow("Vision Navigation", cv_image)
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(f"Image processing failed: {e}")

    def detect_rectangle(self, img):
        # Convert to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define green color range in HSV
        lower_green = np.array([35, 80, 80])
        upper_green = np.array([85, 255, 255])

        # Create a mask that isolates the green pixels
        green_mask = cv2.inRange(hsv, lower_green, upper_green)

        # Clean up the mask to remove noise
        kernel = np.ones((5, 5), np.uint8)
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)

        # Find contours AND their hierarchy
        contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        midpoint_to_publish = None # This will only be set for the actual target

        # --- DEFINE AREA THRESHOLDS ---
        # 1. Minimum area to be considered for DRAWING (filters out noise)
        DRAW_THRESHOLD_AREA = 20000
        # 2. Minimum area for the target to trigger an ACTION
        ACTION_THRESHOLD_AREA = 600000

        # Loop through ALL contours
        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            
            # New: Only process contours that meet the minimum drawing area
            if area > DRAW_THRESHOLD_AREA:
                # Check if the shape is a rectangle (4 vertices)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                if len(approx) == 4:
                    # --- DRAWING STEP (for ALL valid rectangles) ---
                    x, y, w, h = cv2.boundingRect(approx)
                    current_midpoint = (x + w // 2, y + h // 2)
                    
                    # Draw all potential rectangles in green
                    cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)
                    cv2.circle(img, current_midpoint, 5, (255, 255, 0), -1) # Cyan circle
                    # New: Add area text for ALL drawn rectangles
                    cv2.putText(img, f"Area: {int(area)}", (x, y - 15), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # --- ACTION TRIGGER STEP (for the ONE target rectangle) ---
                    is_outermost = hierarchy[0][i][3] == -1
                    
                    if is_outermost and area > ACTION_THRESHOLD_AREA:
                        # This is our target. Store its midpoint to be published.
                        midpoint_to_publish = current_midpoint
                        
                        # Overwrite the drawing and text with a more prominent color for the target
                        cv2.drawContours(img, [approx], 0, (0, 0, 255), 3) # Red for the chosen TARGET
                        cv2.circle(img, current_midpoint, 7, (255, 0, 0), -1) # Blue for the chosen TARGET
                        cv2.putText(img, f"TARGET Area: {int(area)}", (x, y - 15), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # After checking all contours, return the midpoint of the one that met the criteria
        return midpoint_to_publish


def main(args=None):
    rclpy.init(args=args)
    node = VisionNavigation()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
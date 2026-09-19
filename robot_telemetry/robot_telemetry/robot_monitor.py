import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String

class RobotMonitor(Node):
    def __init__(self):
        super().__init__('robot_monitor')

        self.joint1_val = 0.0
        self.joint2_val = 0.0
        self.joint3_val = 0.0

        self.create_subscription(Float64, '/joint1_command', self.joint1_callback, 10)
        self.create_subscription(Float64, '/joint2_command', self.joint2_callback, 10)
        self.create_subscription(Float64, '/joint3_command', self.joint3_callback, 10)

        self.status_pub = self.create_publisher(String, '/robot_status', 10)

    def joint1_callback(self, msg):
        self.joint1_val = msg.data
        self.check_and_publish()

    def joint2_callback(self, msg):
        self.joint2_val = msg.data
        self.check_and_publish()

    def joint3_callback(self, msg):
        self.joint3_val = msg.data
        self.check_and_publish()

    def check_and_publish(self):
        j1_safe = 0 <= self.joint1_val <= 180
        j2_safe = -180 <= self.joint2_val <= 180
        j3_safe = -5 <= self.joint3_val <= 20

        j1_status = "SAFE" if j1_safe else "LIMIT EXCEEDED"
        j2_status = "SAFE" if j2_safe else "LIMIT EXCEEDED"
        j3_status = "SAFE" if j3_safe else "LIMIT EXCEEDED"

        self.get_logger().info(f'Joint 1: {self.joint1_val}° → {j1_status}')
        self.get_logger().info(f'Joint 2: {self.joint2_val}° → {j2_status}')
        self.get_logger().info(f'Joint 3: {self.joint3_val} cm → {j3_status}')

        overall_safe = j1_safe and j2_safe and j3_safe
        overall_status = "SAFE" if overall_safe else "LIMIT EXCEEDED"

        status_str = f'{{"joint1": {self.joint1_val}, "joint2": {self.joint2_val}, "joint3": {self.joint3_val}, "status": "{overall_status}"}}'

        status_msg = String()
        status_msg.data = status_str
        self.status_pub.publish(status_msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

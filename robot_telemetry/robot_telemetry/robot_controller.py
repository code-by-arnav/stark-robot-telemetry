import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')

        self.joint1_pub = self.create_publisher(Float64, '/joint1_command', 10)
        self.joint2_pub = self.create_publisher(Float64, '/joint2_command', 10)
        self.joint3_pub = self.create_publisher(Float64, '/joint3_command', 10)

        self.timer = self.create_timer(1.0, self.publish_commands)

    def publish_commands(self):
        msg1 = Float64()
        msg1.data = 40.0
        self.joint1_pub.publish(msg1)

        msg2 = Float64()
        msg2.data = 225.0
        self.joint2_pub.publish(msg2)

        msg3 = Float64()
        msg3.data = 10.0
        self.joint3_pub.publish(msg3)

        self.get_logger().info(f'Published: J1={msg1.data}, J2={msg2.data}, J3={msg3.data}')

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

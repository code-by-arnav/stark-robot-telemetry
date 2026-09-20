import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

# This node's job is to send out (publish) the position we want each joint to move to.
class RobotController(Node):
    def __init__(self):
        # Set up this node and give it a name.
        super().__init__('robot_controller')

        # Set up one publisher per joint, so we can send a number for each joint on its own separate topic.
        self.joint1_pub = self.create_publisher(Float64, '/joint1_command', 10)
        self.joint2_pub = self.create_publisher(Float64, '/joint2_command', 10)
        self.joint3_pub = self.create_publisher(Float64, '/joint3_command', 10)

        # Every 1 second, automatically run publish_commands().
        self.timer = self.create_timer(1.0, self.publish_commands)

    def publish_commands(self):
        # Send Joint 1's position (in degrees).
        msg1 = Float64()
        msg1.data = 40.0
        self.joint1_pub.publish(msg1)

        # Send Joint 2's position (in degrees).
        # 225 is outside Joint 2's allowed range on purpose so we can see the Monitor node catch it as unsafe.
        msg2 = Float64()
        msg2.data = 225.0
        self.joint2_pub.publish(msg2)

        # Send Joint 3's position (in cm).
        msg3 = Float64()
        msg3.data = 10.0
        self.joint3_pub.publish(msg3)

        # Print what we just sent, so we can see it in the terminal.
        self.get_logger().info(f'Published: J1={msg1.data}, J2={msg2.data}, J3={msg3.data}')

def main(args=None):
    # Start up ROS2, create the node, and keep it running.
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

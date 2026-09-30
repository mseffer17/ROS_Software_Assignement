import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class GPSNode(Node):

    def __init__(self):
        super().__init__('gps_node')
        self.subscription = self.create_subscription(Twist, 'gps_pos', self.position_callback, 10)
        self.get_logger().info('GPS node has been started.')

    def position_callback(self, msg):
        self.get_logger().info(f'Rover position: x={msg.linear.x:.3f}, z={msg.linear.z:.3f}, ry={msg.angular.y:.3f}')


def main(args=None):
    rclpy.init(args=args)
    node = GPSNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
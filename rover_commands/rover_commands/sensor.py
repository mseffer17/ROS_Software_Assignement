import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SensorNode(Node):

    def __init__(self):
        super().__init__('sensor')
        # Publisher des corrections capteurs
        self.publisher_ = self.create_publisher(Twist, 'correction_cmd', 10)

        self.start_time = self.get_clock().now()

        # Timer : ROS appelle publish_correction toutes les 1.0 seconde (sans boucle, sans input)
        self.timer = self.create_timer(1.0, self.publish_correction)

        self.get_logger().info('Sensor node has been started.')

    def publish_correction(self):
        # t = secondes écoulées depuis le démarrage (l'horloge ROS compte en nanosecondes)
        t = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        msg = Twist()
        msg.linear.x = math.sin(t)
        msg.linear.z = math.cos(t)
        msg.angular.y = t

        self.publisher_.publish(msg)
        self.get_logger().info(f'Published correction: x={msg.linear.x:.3f}, z={msg.linear.z:.3f}, ry={msg.angular.y:.3f}.')


def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
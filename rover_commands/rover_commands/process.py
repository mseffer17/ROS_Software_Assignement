import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class ProcessNode(Node):

    def __init__(self):
        super().__init__('process_node')

        # Position courante du rover, gardée en mémoire (tout à 0.0 au départ)
        self.position = Twist()

        # Deux abonnements : la manette et les capteurs
        self.input_sub = self.create_subscription(Twist, 'input_cmd', self.input_callback, 10)
        self.correction_sub = self.create_subscription(Twist, 'correction_cmd', self.correction_callback, 10)

        # Publisher de la position réelle
        self.publisher_ = self.create_publisher(Twist, 'gps_pos', 10)

        # Toutes les secondes, on publie la position courante
        self.timer = self.create_timer(1.0, self.publish_position)

        self.get_logger().info('Process node has been started.')

    def input_callback(self, msg):
        self.get_logger().info('Command received from gamepad')
        self.add_to_position(msg)

    def correction_callback(self, msg):
        self.get_logger().info('Correction received from sensor')
        self.add_to_position(msg)

    def add_to_position(self, msg):
        # Addition champ par champ du Twist reçu à la position courante
        self.position.linear.x += msg.linear.x
        self.position.linear.y += msg.linear.y
        self.position.linear.z += msg.linear.z
        self.position.angular.x += msg.angular.x
        self.position.angular.y += msg.angular.y
        self.position.angular.z += msg.angular.z

    def publish_position(self):
        self.publisher_.publish(self.position)
        p = self.position
        self.get_logger().info(f'Published position: x={p.linear.x:.3f}, z={p.linear.z:.3f}, ry={p.angular.y:.3f}')


def main(args=None):
    rclpy.init(args=args)
    node = ProcessNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TrajectorySubscriber(Node):

    def __init__(self):
        super().__init__('trajectory_subscriber')
        # Un subscriber : type Twist, topic "trajectory", fonction appelée à chaque message, file de 10
        self.subscription = self.create_subscription(Twist, 'trajectory', self.listener_callback, 10)
        self.get_logger().info('Subscriber node has been started.')
        self.position = {'x': 0.0, 'z': 0.0, 'ry': 0.0}

    def listener_callback(self, msg):
        tx = msg.linear.x       # avant (+) / arrière (-)
        tz = msg.linear.z       # glissement : gauche (-) / droite (+)
        ry = msg.angular.y      # rotation sur place : gauche (+) / droite (-)

        # 1) Traduire la commande en phrase, en filtrant les mouvements impossibles
        if (tx and tz) or (tz and ry):
            self.get_logger().info('Forbidden move')
            return                                        # la position ne bouge pas
        if tx and ry:
            text = 'Go ' + ('Left' if ry > 0 else 'Right')
        elif tx:
            text = 'Go ' + ('Forward' if tx > 0 else 'Backward')
        elif tz:
            text = 'Slide ' + ('Left' if tz < 0 else 'Right')
        elif ry:
            text = 'Rotating on itself to the ' + ('Left' if ry > 0 else 'Right')
        else:
            text = 'No move'
        self.get_logger().info(text)

        # 2) Mettre à jour la position : la rotation d'abord, puis la translation
        #    dans la nouvelle orientation (avancer après avoir tourné ne va plus dans la même direction)
        self.position['ry'] += ry
        angle = self.position['ry']
        self.position['x'] += tx * math.cos(angle) + tz * math.sin(angle)
        self.position['z'] += -tx * math.sin(angle) + tz * math.cos(angle)
        self.position = {k: round(v, 3) for k, v in self.position.items()}
        self.get_logger().info(f'New Position: {self.position}')


def main(args=None):
    rclpy.init(args=args)
    node = TrajectorySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
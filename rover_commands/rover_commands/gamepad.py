import rclpy                       # la bibliothèque ROS 2 pour Python
from rclpy.node import Node        # la classe de base de tout nœud
from geometry_msgs.msg import Twist  # le type de message : vitesse linéaire + angulaire

# Chaque lettre = (axe du message, valeur). +1 / -1 donnent le sens.
COMMANDS = {
    'w': ('linear.x', 1.0),    # avancer
    's': ('linear.x', -1.0),   # reculer
    'a': ('linear.z', -1.0),   # glisser à gauche
    'd': ('linear.z', 1.0),    # glisser à droite
    't': ('angular.y', 1.0),   # tourner à gauche
    'y': ('angular.y', -1.0),  # tourner à droite
}


class GamepadNode(Node):

    def __init__(self):
        super().__init__('gamepad')        # nom du nœud dans ROS
        # Un publisher : type de message Twist, topic "trajectory", file d'attente de 10 messages
        self.publisher_ = self.create_publisher(Twist, 'input_cmd', 10)
        self.get_logger().info('Gamepad node has been started.')

        # Boucle : on demande une commande, on l'envoie, et on recommence (Ctrl+C pour arrêter)
        while rclpy.ok():
            self.cmd_acquisition()

    def cmd_acquisition(self):
        command = input("Enter command (w/a/s/d/t/y): ").strip().lower()
        if command not in COMMANDS:                       # vide, ou lettre inconnue
            self.get_logger().warn(f'Unknown command: {command}')
            return
        msg = Twist()                                     # tout est à 0.0 au départ
        axis, value = COMMANDS[command]
        part, coord = axis.split('.')                     # 'linear.x' -> 'linear' et 'x'
        setattr(getattr(msg, part), coord, value)         # équivaut à msg.linear.x = 1.0
        self.publisher_.publish(msg)                      # envoi sur le topic
        self.get_logger().info(f'Published: {msg}')


def main(args=None):
    rclpy.init(args=args)
    node = GamepadNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
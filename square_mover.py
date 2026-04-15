#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SquareMover(Node):

    def __init__(self):
        super().__init__('square_mover')

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.SPEED = 1.0
        self.TURN_SPEED = 1.0
        self.SIDE_LENGTH = 2.0

        self.MOVE_TIME = self.SIDE_LENGTH / self.SPEED
        self.TURN_TIME = 1.5708 / self.TURN_SPEED

        self.get_logger().info('节点启动')

    def publish_for_duration(self, linear, angular, duration):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular

        start = self.get_clock().now()

        while (self.get_clock().now() - start).nanoseconds < duration * 1e9:
            self.publisher_.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.01)  # ✅ 关键

        self.stop()

    def stop(self):
        msg = Twist()
        self.publisher_.publish(msg)

    def move_square(self):
        for i in range(4):
            self.get_logger().info(f'边 {i+1}')
            self.publish_for_duration(self.SPEED, 0.0, self.MOVE_TIME)

            self.get_logger().info(f'转弯 {i+1}')
            self.publish_for_duration(0.0, self.TURN_SPEED, self.TURN_TIME)


def main():
    rclpy.init()
    node = SquareMover()

    node.move_square()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

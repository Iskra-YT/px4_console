from px4_msgs.msg import VehicleLocalPosition
from px4_msgs.msg import TrajectorySetpoint
from px4_msgs.msg import OffboardControlMode
from px4_msgs.msg import VehicleCommand

import math
import threading

import rclpy
from rclpy.node import Node

class CommanderNode(Node):
    def __init__(self):
        super().__init__('commander_node')
        
        self.create_subscription(
            VehicleLocalPosition,
            "/fmu/out/vehicle_local_position",
            self.position_callback,
            10
        )

        self.trajectory_publisher = self.create_publisher(
            TrajectorySetpoint,
            "/fmu/in/trajectory_setpoint",
            10
        )

        self.command_publisher = self.create_publisher(
            VehicleCommand,
            "/fmu/in/vehicle_command",
            10
        )

        self.offboard_publisher = self.create_publisher(
            OffboardControlMode,
            "/fmu/in/offboard_control_mode",
            10
        )

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.current_position = [0.0, 0.0, 0.0]
        self.target_position = [0.0, 0.0, 0.0]

        self.current_yaw = 0.0
        self.target_yaw = 0.0

        self.get_logger().info("CommanderNode initialized")

        self.command_thread = threading.Thread(target=self.command_loop, daemon=True)
        self.command_thread.start()

    def publish_offboard_mode(self):
        msg = OffboardControlMode()
        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False

        self.offboard_publisher.publish(msg)
    
    def position_callback(self, msg):
        self.current_position = [msg.x, msg.y, msg.z]
        self.current_yaw = msg.heading

    def timer_callback(self):
        self.publish_offboard_mode()

        setpoint = TrajectorySetpoint()

        setpoint.timestamp = int(
            self.get_clock().now().nanoseconds / 1000
        )

        setpoint.position = self.target_position
        setpoint.yaw = self.target_yaw

        self.trajectory_publisher.publish(setpoint)

    def enable_offboard(self):
        msg = VehicleCommand()

        msg.command = VehicleCommand.VEHICLE_CMD_DO_SET_MODE
        msg.param1 = 1.0
        msg.param2 = 6.0

        self.command_publisher.publish(msg)

        self.get_logger().info('OFFBOARD enabled')

    def arm(self):
        msg = VehicleCommand()

        msg.command = VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM
        msg.param1 = 1.0

        self.command_publisher.publish(msg)

        self.get_logger().info('Vehicle armed')

    def command_loop(self):
        while rclpy.ok():
            try:
                command = input("px4_console> ").strip().lower()
                tokens = command.split()
                if len(tokens) == 0:
                    continue

                if tokens[0] == "arm":
                    self.arm()
                elif tokens[0] == "offboard":
                    self.enable_offboard()
                elif tokens[0] == "start":
                    self.arm()
                    self.enable_offboard()

                elif tokens[0] == "forward":
                    distance = float(tokens[1]) if len(tokens) > 1 else 1.0
                    self.forward(distance)
                elif tokens[0] == "back":
                    distance = float(tokens[1]) if len(tokens) > 1 else 1.0
                    self.forward(-distance)
                
                elif tokens[0] == "yaw":
                    angle = float(tokens[1]) if len(tokens) > 1 else 15.0
                    self.yaw(angle)

                elif tokens[0] == "up":
                    distance = float(tokens[1]) if len(tokens) > 1 else 5.0
                    self.up(distance)
                else:
                    self.get_logger().info(f"Unknown command: {tokens[0]}")

            except EOFError:
                self.get_logger().info("Exiting command loop")
                break

            except Exception as e:
                self.get_logger().error(f"Error processing command: {e}")

    def forward(self, distance):
        self.target_position[0] += distance * math.cos(self.current_yaw)
        self.target_position[1] += distance * math.sin(self.current_yaw)

    def up(self, distance):
        self.target_position[2] -= distance

    def yaw(self, angle_deg):
        self.target_yaw += math.radians(angle_deg)

        while self.target_yaw > math.pi:
            self.target_yaw -= 2 * math.pi

        while self.target_yaw < -math.pi:
            self.target_yaw += 2 * math.pi

def main(args=None):
    rclpy.init(args=args)
    node = CommanderNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
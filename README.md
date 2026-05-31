# PX4 Console

PX4 Console is an open-source command-line interface for PX4 Autopilot built on ROS 2. It allows users to control drones using simple text commands.

## Features

- Arm and disarm vehicles
- Enable Offboard mode
- Move the drone using simple commands
- Rotate the drone using yaw commands
- ROS 2 and PX4 integration
- Designed for simulation and real-world testing

## Requirements

- ROS 2 Humble (or newer)
- PX4 Autopilot
- px4_msgs

## Installation

Clone the repository:

```bash
git clone https://github.com/Iskra-YT/px4_console.git
cd px4_console
```

Build:

```bash
colcon build
```

## Usage

Source the workspace:

```bash
source install/setup.bash
```

Run the console:

```bash
ros2 run px4_console console
```

## Commands

- `arm`: Arm the vehicle
- `disarm`: Disarm the vehicle
- `offboard`: Enable Offboard mode
- `start`: Arm the vehicle and enable Offboard mode
- `forward <distance>`: Move forward by a specified distance (in meters)
- `backward <distance>`: Move backward by a specified distance (in meters)
- `yaw <angle>`: Rotate the drone by a specified angle (in degrees)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

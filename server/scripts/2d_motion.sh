#!/bin/bash

# 启动hector slam
roslaunch hector_slam_launch hector_slam_xtdrone.launch &

# 等待几秒确保启动完成
sleep 5

# 启动坐标转换
cd ~/XTDrone/sensing/slam/laser_slam/script
python3 laser_transfer.py iris 0 hector &

# 启动2D运动规划
cd ~/XTDrone/motion_planning/2d/launch
roslaunch 2d_motion_planning.launch &

# 启动通信和控制
cd ~/XTDrone/communication
python3 multirotor_communication.py iris 0 &

cd ~/XTDrone/control/keyboard
python3 multirotor_keyboard_control.py iris 1 vel 
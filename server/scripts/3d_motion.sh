#!/bin/bash

# 启动VINS-Fusion
cd ~/catkin_ws
bash scripts/xtdrone_run_vio.sh &

sleep 5

# 启动坐标转换
cd ~/XTDrone/sensing/slam/vio
python3 vins_transfer.py iris 0 &

# 启动ego planner坐标转换
cd ~/XTDrone/motion_planning/3d
python3 ego_transfer.py iris 0 &

# 启动ego planner可视化
rviz -d ego_rviz.rviz &

# 启动规划器
roslaunch ego_planner single_uav.launch &

# 启动通信和控制
cd ~/XTDrone/communication
python3 multirotor_communication.py iris 0 &

cd ~/XTDrone/control/keyboard
python3 multirotor_keyboard_control.py iris 1 vel 
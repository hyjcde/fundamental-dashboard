#!/bin/bash

# 启动VINS-Fusion
cd ~/catkin_ws
bash scripts/xtdrone_run_vio.sh &

# 等待几秒确保VINS启动
sleep 5

# 启动坐标转换
cd ~/XTDrone/sensing/slam/vio
python3 vins_transfer.py iris 0 &

# 启动通信
cd ~/XTDrone/communication
python3 multirotor_communication.py iris 0 &

# 启动键盘控制
cd ~/XTDrone/control/keyboard
python3 multirotor_keyboard_control.py iris 1 vel 
# System Control Backend

这是一个简单的后端服务，用于控制ROS系统的启动和停止。

## 功能特点

- 支持多种启动模式（SLAM VINS、2D Motion、3D Motion）
- 自动管理进程生命周期
- 提供RESTful API接口
- 支持跨域请求
- 自动处理脚本权限


python app.py

服务将在 http://localhost:5000 启动

## API接口

### 1. 启动系统

- **URL**: `/api/system/start`
- **Method**: `POST`
- **Data**:
  ```json
  {
    "mode": "slam_vins" // 可选值: "slam_vins", "2d_motion", "3d_motion"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Started slam_vins mode"
  }
  ```

### 2. 停止系统

- **URL**: `/api/system/stop`
- **Method**: `POST`
- **Response**:
  ```json
  {
    "success": true,
    "message": "System stopped"
  }
  ```

## 注意事项

1. 确保系统已安装ROS和相关依赖
2. 确保脚本中的路径与实际环境匹配
3. 需要正确配置gzweb环境
4. 建议在使用前测试各个脚本是否能单独正常运行

## 错误处理

服务会自动处理以下情况：
- 启动失败
- 进程终止
- 权限问题
- 路径错误

所有错误都会返回带有错误信息的JSON响应。

## 开发说明

1. 添加新的启动模式：
   - 在 `scripts` 文件夹中添加新的 `.sh` 脚本
   - 脚本命名应该与mode参数对应

2. 修改现有脚本：
   - 直接编辑 `scripts` 文件夹中的相应脚本
   - 注意保持后台运行命令的 `&` 符号

3. 调试提示：
   - 检查 Flask 服务的控制台输出
   - 检查各个脚本的输出重定向
   - 使用 `ps aux | grep` 命令检查进程状态
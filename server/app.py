import os
import signal
import subprocess

import psutil
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 存储进程ID
running_processes = []

# 获取脚本的绝对路径
def get_script_path(script_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'scripts', script_name)

@app.route('/api/system/start', methods=['POST'])
def start_system():
    mode = request.json.get('mode', 'slam_vins')
    try:
        # 停止所有正在运行的进程
        stop_all_processes()
        
        # 启动选择的模式
        script_path = get_script_path(f'{mode}.sh')
        
        # 确保脚本有执行权限
        os.chmod(script_path, 0o755)
        
        # 启动脚本
        process = subprocess.Popen(['bash', script_path], 
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        running_processes.append(process.pid)
        
        # 启动gzweb
        gzweb_process = subprocess.Popen(
            'cd ~/gzweb && . ~/.nvm/nvm.sh && nvm use 11 && npm start',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        running_processes.append(gzweb_process.pid)
        
        return jsonify({
            'success': True,
            'message': f'Started {mode} mode'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/api/system/stop', methods=['POST'])
def stop_system():
    try:
        stop_all_processes()
        return jsonify({
            'success': True,
            'message': 'System stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

def stop_all_processes():
    # 停止存储的进程
    for pid in running_processes:
        try:
            process = psutil.Process(pid)
            process.terminate()
        except:
            pass
    
    # 清空进程列表
    running_processes.clear()
    
    # 使用pkill停止相关进程
    try:
        subprocess.run(['pkill', '-f', 'ros'])
        subprocess.run(['pkill', '-f', 'gzserver'])
        subprocess.run(['pkill', '-f', 'npm'])
    except:
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
<template>
  <div class="tasks-container">
    <!-- 步骤条 -->
    <el-steps :active="1" finish-status="success" simple class="steps">
      <el-step title="Select Modules"></el-step>
      <el-step title="Import Tasks"></el-step>
      <el-step title="Task Execution"></el-step>
    </el-steps>

    <div class="main-content">
      <!-- 左侧内容区域 -->
      <div class="left-panel">
        <!-- 系统参数配置 -->
        <div class="system-config">
          <!-- System Selection Section -->
          <div class="config-section">
            <div class="section-header">
              <div class="section-title">System selection</div>
              <div class="section-subtitle">Please select robot first, then sensors</div>
            </div>
            
            <div class="selection-list">
              <!-- Robot Selection -->
              <div class="selection-item">
                <div class="item-label">Robot</div>
                <el-select v-model="config.robot" size="small" placeholder="Select robot" @change="handleRobotChange">
                  <el-option label="Numerical sim" value="numerical"></el-option>
                  <el-option label="Gazebo" value="gazebo"></el-option>
                  <el-option label="Real Robot" value="real"></el-option>
                </el-select>
              </div>

              <!-- Sensors Selection -->
              <div class="selection-item">
                <div class="item-label">Sensors</div>
                <el-select 
                  v-model="config.sensors" 
                  size="small" 
                  multiple 
                  collapse-tags
                  :disabled="!config.robot"
                  placeholder="Select sensors"
                >
                  <el-option label="Lidar" value="lidar"></el-option>
                  <el-option label="IMU" value="imu"></el-option>
                  <el-option label="Camera" value="camera"></el-option>
                </el-select>
              </div>

              <!-- Other Selections -->
              <div class="selection-item">
                <div class="item-label">Task planner</div>
                <el-select 
                  v-model="config.taskPlanner" 
                  size="small" 
                  placeholder="Select task planner"
                  :disabled="!config.robot"
                >
                  <el-option label="RT-LTL (CUHK)" value="rt-ltl"></el-option>
                  <el-option label="LTL Planner" value="ltl"></el-option>
                  <el-option label="STL Planner" value="stl"></el-option>
                </el-select>
              </div>

              <div class="selection-item">
                <div class="item-label">Motion planner</div>
                <el-select 
                  v-model="config.motionPlanner" 
                  size="small" 
                  placeholder="Select motion planner"
                  :disabled="!config.robot"
                >
                  <el-option label="BSCP (NUS)" value="bscp"></el-option>
                  <el-option label="RRT" value="rrt"></el-option>
                  <el-option label="PRM" value="prm"></el-option>
                  <el-option label="A*" value="astar"></el-option>
                </el-select>
              </div>

              <div class="selection-item">
                <div class="item-label">Workspace</div>
                <el-select 
                  v-model="config.workspace" 
                  size="small" 
                  placeholder="Select workspace"
                  :disabled="!config.robot"
                >
                  <el-option label="Vicon room" value="vicon"></el-option>
                  <el-option label="Simulation" value="sim"></el-option>
                  <el-option label="Outdoor" value="outdoor"></el-option>
                </el-select>
              </div>

              <div class="selection-item">
                <div class="item-label">Localization</div>
                <el-select 
                  v-model="config.localization" 
                  size="small" 
                  placeholder="Select localization"
                  :disabled="!config.robot"
                >
                  <el-option label="ORB-SLAM3" value="orbslam"></el-option>
                  <el-option label="VINS" value="vins"></el-option>
                  <el-option label="GPS/IMU" value="gps"></el-option>
                </el-select>
              </div>
            </div>

            <div class="action-buttons">
              <el-button size="small" type="primary" @click="showConfirmDialog">Confirm Selection</el-button>
              <el-button size="small" @click="resetSelection">Reset</el-button>
            </div>
          </div>

          <!-- System Control -->
          <div class="config-section">
            <div class="section-header">
              <div class="section-title">System Control</div>
            </div>
            <system-control
              @system-started="handleSystemStarted"
              @system-stopped="handleSystemStopped"
            />
          </div>

          <!-- Task Panel Section -->
          <div class="config-section task-panel">
            <div class="section-header">
              <div class="section-title">Task panel</div>
            </div>
            <div class="button-group">
              <el-button size="small" type="success">Record</el-button>
              <el-button size="small" type="danger">Stop</el-button>
              <el-button size="small" type="warning">Replay</el-button>
            </div>
          </div>
        </div>

        <!-- 系统输出区域 -->
        <div class="output-area">
          <div class="output-header">
            <span>System Output</span>
            <el-button size="small" type="text" @click="clearOutput">Clear</el-button>
          </div>
          <el-input
            type="textarea"
            :rows="8"
            v-model="systemOutput"
            readonly
            class="output-content"
          ></el-input>
        </div>
      </div>

      <!-- 右侧 GZWeb 区域 -->
      <div class="right-panel">
        <div class="gzweb-container">
          <iframe 
            src="http://localhost:8080"
            frameborder="0"
            class="gzweb-frame"
          ></iframe>
        </div>
      </div>
    </div>

    <!-- 确认对话框 -->
    <el-dialog
      title="Confirm System Configuration"
      :visible.sync="dialogVisible"
      width="500px"
    >
      <el-table :data="configTableData" style="width: 100%">
        <el-table-column prop="item" label="Item" width="180"></el-table-column>
        <el-table-column prop="value" label="Selected Value"></el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="confirmConfig">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import SystemControl from '@/components/SystemControl.vue'

export default {
  name: 'Tasks',
  components: {
    SystemControl
  },
  data() {
    return {
      config: {
        robot: '',
        sensors: [],
        taskPlanner: '',
        motionPlanner: '',
        workspace: '',
        localization: ''
      },
      systemOutput: 'System initialization...\nLoading modules...\nReady.',
      dialogVisible: false
    }
  },
  computed: {
    configTableData() {
      return [
        { item: 'Robot', value: this.config.robot },
        { item: 'Sensors', value: this.config.sensors.join(', ') },
        { item: 'Task Planner', value: this.config.taskPlanner },
        { item: 'Motion Planner', value: this.config.motionPlanner },
        { item: 'Workspace', value: this.config.workspace },
        { item: 'Localization', value: this.config.localization }
      ]
    }
  },
  methods: {
    handleRobotChange(value) {
      if (!value) {
        this.resetSelection(true)
      }
    },
    showConfirmDialog() {
      if (!this.config.robot) {
        this.$message.warning('Please select a robot first')
        return
      }
      this.dialogVisible = true
    },
    confirmConfig() {
      this.dialogVisible = false
      this.$message.success('Configuration confirmed')
      this.systemOutput += '\nConfiguration applied successfully.'
    },
    resetSelection(keepRobot = false) {
      this.config = {
        robot: keepRobot ? this.config.robot : '',
        sensors: [],
        taskPlanner: '',
        motionPlanner: '',
        workspace: '',
        localization: ''
      }
    },
    clearOutput() {
      this.systemOutput = ''
    },
    handleSystemStarted() {
      this.systemOutput += '\nSystem started successfully'
      // 可以在这里添加其他启动后的逻辑
    },
    handleSystemStopped() {
      this.systemOutput += '\nSystem stopped'
      // 可以在这里添加其他停止后的逻辑
    }
  }
}
</script>

<style scoped>
.tasks-container {
  padding: 20px;
  height: calc(100vh - 84px);
  display: flex;
  flex-direction: column;
}

.steps {
  margin-bottom: 20px;
}

.main-content {
  display: flex;
  gap: 20px;
  flex: 1;
  min-height: 0;
}

.left-panel {
  width: 580px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-panel {
  flex: 1;
  min-width: 0;
}

.system-config {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 15px;
}

.config-section {
  margin-bottom: 15px;
  padding: 15px;
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.config-section:last-child {
  margin-bottom: 0;
}

.section-header {
  margin-bottom: 15px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.section-subtitle {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.selection-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr) auto;
  gap: 12px;
  align-items: flex-end;
}

.selection-item {
  min-width: 0;
}

.item-label {
  font-size: 12px;
  color: #606266;
  margin-bottom: 4px;
}

.action-item {
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
}

:deep(.el-select) {
  width: 100%;
}

.task-panel {
  text-align: center;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.output-area {
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.output-header {
  padding: 10px 15px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  font-weight: 500;
}

.output-content {
  flex: 1;
  margin: 10px;
}

.output-content :deep(.el-textarea__inner) {
  font-family: 'Menlo', 'Monaco', 'Consolas', monospace;
  background: #f5f7fa;
  font-size: 12px;
  line-height: 1.6;
}

.gzweb-container {
  height: 100%;
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.gzweb-frame {
  width: 100%;
  height: 100%;
}

.selection-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.selection-item {
  width: 100%;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

/* 确保下拉框样式统一 */
:deep(.el-select) {
  width: 100%;
}

:deep(.el-select .el-input__inner) {
  height: 32px;
  line-height: 32px;
}

/* 调整多选标签的样式 */
:deep(.el-select__tags) {
  height: 24px;
  overflow: hidden;
}
</style> 
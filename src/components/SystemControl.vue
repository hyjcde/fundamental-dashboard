<template>
  <div class="system-control">
    <div class="control-buttons">
      <el-button 
        type="primary" 
        :loading="isStarting"
        @click="startSystem"
      >
        {{ isStarting ? 'Starting...' : 'System Start' }}
      </el-button>
      <el-button 
        type="danger" 
        :disabled="!isSystemRunning"
        @click="stopSystem"
      >
        Stop System
      </el-button>
    </div>
    
    <!-- 启动选项对话框 -->
    <el-dialog
      title="Start System"
      :visible.sync="startDialogVisible"
      width="400px"
    >
      <el-form :model="startOptions" label-width="120px">
        <el-form-item label="Start Mode">
          <el-radio-group v-model="startOptions.mode">
            <el-radio label="slam_vins">SLAM VINS</el-radio>
            <el-radio label="2d_motion">2D Motion</el-radio>
            <el-radio label="3d_motion">3D Motion</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="startDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="confirmStart">Start</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import request from '@/utils/request'

export default {
  name: 'SystemControl',
  data() {
    return {
      isStarting: false,
      isSystemRunning: false,
      startDialogVisible: false,
      startOptions: {
        mode: 'slam_vins'
      }
    }
  },
  methods: {
    startSystem() {
      this.startDialogVisible = true
    },
    async confirmStart() {
      this.startDialogVisible = false
      this.isStarting = true
      try {
        const response = await request({
          url: '/api/system/start',
          method: 'post',
          data: {
            mode: this.startOptions.mode
          }
        })
        
        if (response.success) {
          this.$message.success('System started successfully')
          this.isSystemRunning = true
          this.$emit('system-started')
        } else {
          throw new Error(response.message)
        }
      } catch (error) {
        this.$message.error(`Failed to start system: ${error.message}`)
      } finally {
        this.isStarting = false
      }
    },
    async stopSystem() {
      try {
        const response = await request({
          url: '/api/system/stop',
          method: 'post'
        })
        if (response.success) {
          this.$message.success('System stopped successfully')
          this.isSystemRunning = false
          this.$emit('system-stopped')
        } else {
          throw new Error(response.message)
        }
      } catch (error) {
        this.$message.error(`Failed to stop system: ${error.message}`)
      }
    }
  }
}
</script>

<style scoped>
.system-control {
  margin-bottom: 15px;
}

.control-buttons {
  display: flex;
  gap: 10px;
}
</style> 
<template>
  <div class="guide-container">
    <h2>Guide</h2>
    <div class="guide-content">
      <!-- 指南内容 -->
      <el-card class="guide-card">
        <h3>Getting Started</h3>
        <p>Follow these steps to get started with the system:</p>
        <ol>
          <li>Select the required modules from the Tasks page</li>
          <li>Import your tasks</li>
          <li>Execute and monitor your tasks</li>
        </ol>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Guide',
  data() {
    return {
      // 数据
    }
  }
}
</script>

<style scoped>
.guide-container {
  padding: 20px;
}

.guide-content {
  margin-top: 20px;
}

.guide-card {
  max-width: 800px;
  margin: 0 auto;
}

.guide-card h3 {
  margin-bottom: 15px;
}

.guide-card ol {
  padding-left: 20px;
  line-height: 1.8;
}
</style> 
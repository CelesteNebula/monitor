<template>
  <div id="app">
    <header>
      <h1>车辆监控系统</h1>
    </header>
    <div class="main-container">
      <aside>
        <button @click="startMonitoring">开始监控</button>
        <button @click="stopMonitoring">结束监控</button>
        <button @click="toggleStats">统计数据</button>
        <div class="sidebar-icon">
          <i class="fas fa-power-off"></i>
        </div>
        <div class="sidebar-icon">
          <i class="fas fa-sync-alt"></i>
        </div>
        <div class="sidebar-icon">
          <i class="fas fa-list"></i>
        </div>
      </aside>
      <main>
        <div class="grid-container">
          <div class="grid-item">
            <VideoMonitor title="监控视频1" streamName="video1" />
          </div>
          <div class="grid-item">
            <VehicleCarousel title="截取到车辆图片1" streamName="video1" />
          </div>
          <div class="grid-item">
            <VideoMonitor title="监控视频2" streamName="video2" />
          </div>
          <div class="grid-item">
            <VehicleCarousel title="截取到车辆图片2" streamName="video2" />
          </div>
        </div>
        <VehicleStats v-if="showStatsDialog" @close="showStatsDialog = false" />
      </main>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import VideoMonitor from './components/VideoMonitor.vue';
import VehicleCarousel from './components/VehicleCarousel.vue';
import VehicleStats from './components/VehicleStats.vue';

export default {
  components: {
    VideoMonitor,
    VehicleCarousel,
    VehicleStats
  },
  data() {
    return {
      showStatsDialog: false
    };
  },
  methods: {
    startMonitoring() {
      axios.post('http://localhost:5000/start_monitoring')
        .then(response => {
          if (response.data.status === 'started') {
            alert('监控已开始');
          } else if (response.data.status === 'already started') {
            alert('监控已经在运行');
          }
        })
        .catch(error => {
          console.error('启动监控失败:', error);
        });
    },
    stopMonitoring() {
      axios.post('http://localhost:5000/stop_monitoring')
        .then(response => {
          if (response.data.status === 'stopped') {
            alert('监控已结束');
          } else if (response.data.status === 'not started') {
            alert('监控未运行');
          }
        })
        .catch(error => {
          console.error('停止监控失败:', error);
        });
    },
    toggleStats() {
      this.showStatsDialog = !this.showStatsDialog;
    }
  }
};
</script>

<style>
/* 样式保持不变 */
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

header {
  background-color: #555;
  color: white;
  text-align: center;
  padding: 1rem;
}

.main-container {
  display: flex;
  flex: 1;
  align-items: stretch;
}

aside {
  display: flex;
  flex-direction: column;
  background-color: #aaa;
  padding: 1rem;
  align-items: center;
  width: 80px;
  justify-content: flex-start;
}

.sidebar-icon {
  margin: 1rem 0;
  font-size: 1.5rem;
  cursor: pointer;
}

main {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background-color: #f0f0f0;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-gap: 1rem;
  flex: 1;
}

.grid-item {
  background-color: #ddd;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 1rem;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  margin-bottom: 1rem;
}

button:hover {
  background-color: #0056b3;
}

/* 统计数据弹窗样式 */
.stats-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.stats-content {
  background-color: #fff;
  padding: 2rem;
  border-radius: 8px;
  max-width: 600px;
  width: 100%;
  max-height: 80%; /* 设置最大高度 */
  overflow-y: auto; /* 启用垂直滚动条 */
}

.close-btn {
  background-color: #ff0000;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  margin-bottom: 1rem;
}

.close-btn:hover {
  background-color: #cc0000;
}

h2 {
  margin-top: 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

th, td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

h3 {
  margin-top: 1rem;
}
</style>

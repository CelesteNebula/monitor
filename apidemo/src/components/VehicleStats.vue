<template>
  <div class="stats-dialog">
    <div class="stats-content">
      <button class="close-btn" @click="$emit('close')">关闭</button>
      <h2>车辆统计</h2>
      <div v-for="(data, video) in stats" :key="video">
        <h3>{{ video }}</h3>
        <table>
          <thead>
            <tr>
              <th>类型</th>
              <th>数量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(count, type) in data" :key="type">
              <td>{{ type }}</td>
              <td>{{ count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <h2>车流量</h2>
      <p>{{ traffic }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'VehicleStats',
  data() {
    return {
      stats: {},
      traffic: 0
    };
  },
  mounted() {
    this.fetchStats();
    this.fetchTraffic();
    setInterval(() => {
      this.fetchStats();
      this.fetchTraffic();
    }, 5000);
  },
  methods: {
    fetchStats() {
      axios.get('http://localhost:5000/stats')
        .then(response => {
          this.stats = response.data;
        })
        .catch(error => {
          console.error('获取统计数据失败:', error);
        });
    },
    fetchTraffic() {
      axios.get('http://localhost:5000/traffic')
        .then(response => {
          this.traffic = response.data.traffic;
        })
        .catch(error => {
          console.error('获取车流量数据失败:', error);
        });
    }
  }
};
</script>

<style scoped>
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
  max-height: 80%;
  overflow-y: auto;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.close-btn {
  background-color: #ff0000;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  margin-bottom: 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
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

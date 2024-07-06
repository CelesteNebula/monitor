<template>
  <div>
    <h2>{{ title }}</h2>
    <div class="carousel">
      <div v-for="(vehicle, index) in vehicles" :key="index" class="carousel-item">
        <img :src="'data:image/jpeg;base64,' + vehicle.image" alt="Vehicle Image" />
        <p>{{ vehicle.name }} ({{ vehicle.type }})</p>
        <p>年份: {{ vehicle.year }}</p>
        <p>颜色: {{ vehicle.color }}</p>
        <p>置信度: {{ (vehicle.score * 100).toFixed(2) }}%</p>
      </div>
    </div>
  </div>
</template>

<script>
import { io } from "socket.io-client";

const socket = io('http://localhost:5000');

export default {
  name: 'VehicleCarousel',
  props: ['streamName'],
  data() {
    return {
      vehicles: []
    };
  },
  mounted() {
    socket.on(`${this.streamName}_recognized`, (data) => {
      this.vehicles.push(data);
      if (this.vehicles.length > 3) {
        this.vehicles.shift();
      }
    });
  }
};
</script>

<style scoped>
.carousel {
  display: flex;
  overflow-x: auto;
  white-space: nowrap;
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.carousel-item {
  flex: 0 0 auto;
  margin-right: 10px;
  cursor: pointer;
  background-color: #fff;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.carousel-item img {
  width: 100px;
  height: auto;
  border-radius: 4px;
}
</style>

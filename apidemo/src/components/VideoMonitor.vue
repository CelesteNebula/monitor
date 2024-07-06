<template>
  <div>
    <h2>{{ title }}</h2>
    <img :src="videoFrame" alt="Video Stream" />
  </div>
</template>

<script>
import socket from '../socket';

export default {
  props: ['title', 'streamName'],
  data() {
    return {
      videoFrame: ''
    };
  },
  mounted() {
    socket.on(`${this.streamName}_frame`, (data) => {
      this.videoFrame = `data:image/jpeg;base64,${data.frame}`;
    });
  }
};
</script>

<style scoped>
img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>

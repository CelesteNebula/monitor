<!-- src/components/Monitor.vue -->
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
  }
  </style>
  
// src/socket.js
import io from 'socket.io-client';

const socket = io('http://localhost:5000'); // 连接后端WebSocket服务器

export default socket;

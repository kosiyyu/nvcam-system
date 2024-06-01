<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import { ref, onMounted, onUnmounted } from "vue";
import { io, Socket } from "socket.io-client";
import { isAuthenticated } from "@/utils/authUtils";
import { isSocket } from "@/utils/dashboardUtils";

const ip = import.meta.env.IP;

interface SensorData {
  temp: string;
  humidity: string;
  controller_temp: string;
}

let isPlaying = ref(true);
let imageUrl = ref('');
let sensorData = ref<SensorData>({ temp: "-", humidity: "-", controller_temp: "-" });

let cameraSocket: Socket | unknown = null;
let motorSocket: Socket | unknown = null;
let sensorSocket: Socket | unknown = null;

onMounted(() => {
  cameraSocket = io('http://localhost:8003');
  motorSocket = io(`http://${ip}:12345`);
  sensorSocket = io(`http://${ip}:12344`);

  if (!isSocket(cameraSocket)) {
    return;
  }

  if (!isSocket(sensorSocket)) {
    return;
  }

  if (!isSocket(motorSocket)) {
    return;
  }

  cameraSocket.on('frame', (data) => {
    if (!isPlaying.value) return;
    // console.log(`Received frame of size: ${data.byteLength} bytes`);
    const uint8Array = new Uint8Array(data);
    const blob = new Blob([uint8Array], { type: 'image/jpeg' });
    imageUrl.value = URL.createObjectURL(blob);
  });

  sensorSocket.on('sensor_data', (data) => {
    // console.log(data);
    sensorData.value = data;
  });
});

onUnmounted(() => {
  if (isSocket(cameraSocket)) {
    cameraSocket.disconnect();
  }

  if (isSocket(sensorSocket)) {
    sensorSocket.disconnect();
  }

  if (isSocket(motorSocket)) {
    motorSocket.disconnect();
  }
});

function playVideo() {
  isPlaying.value = true;
}

function pauseVideo() {
  isPlaying.value = false;
}

function move(direction: string) {
  if (isSocket(motorSocket)) {
    motorSocket.emit('move', direction);
  }
}
</script>

<template>
  <NavBar :is-authenticated="isAuthenticated" />
  <main class="bg-green-950 flex flex-col items-center h-screen">
    <div class="flex space-x-4">
      <div class="flex flex-col items-center m-4">
        <div class="w-[640px] h-[360px] object-cover bg-black">
          <img :src="imageUrl">
        </div>
        <div class="mt-2">
          <div v-if="isPlaying">
            <button @click="pauseVideo"
              class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-full">
              Pause
            </button>
          </div>
          <div v-else>
            <button @click="playVideo"
              class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-full">
              Play
            </button>
          </div>
        </div>
      </div>
      <div class="my-4">
        <div class="w-[300px] bg-special-pink text-black font-bold rounded-lg p-4 mb-2 overflow-auto whitespace-normal">
          <div>Controller temperature: {{ sensorData.controller_temp }} °C</div>
          <div>Sensor temperature: {{ sensorData.temp }} °C</div>
          <div>Sensor humidity: {{ sensorData.humidity }} RH</div>
        </div>
        <div class="flex justify-between">
          <button @click="move('left')" class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-full">Move Left</button>
          <button @click="move('right')" class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-full">Move Right</button>
        </div>
      </div>
    </div>
  </main>
  <footer class="bg-black">
    footer
  </footer>
</template>
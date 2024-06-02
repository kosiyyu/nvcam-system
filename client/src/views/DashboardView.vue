<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import { ref, onMounted, onUnmounted } from "vue";
import { io, Socket } from "socket.io-client";
import { isAuthenticated } from "@/utils/authUtils";
import { isSocket } from "@/utils/dashboardUtils";
import axios from "axios";

const ip = import.meta.env.IP;

interface SensorData {
  temp: string;
  humidity: string;
  controller_temp: string;
}

let images = ref<string[]>([]);
let page = ref(1);

const prevPage = async () => {
  if (page.value > 1) {
    const tempPage = page.value - 1;
    try {
      await fetchImages(tempPage);
      page.value = tempPage;
    } catch (error) {
      page.value = 1;
      console.error(error);
    }
  }
};

const nextPage = async () => {
  const tempPage = page.value + 1;
  try {
    await fetchImages(tempPage);
    page.value = tempPage;
  } catch (error) {
    page.value = 1;
    console.error(error);
  }
};

const fetchImages = async (tempPage: number) => {
  console.log(tempPage);
  axios(`http://localhost:8003/page/${tempPage}`)
  .then(response => {
    const data = response.data;
    images.value = data.images.map((image: string) => 'data:image/jpeg;base64,' + image);
  })
  .catch(error => {
    console.error(error);
    page.value = 1;
  });
};

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
    <div class="flex flex-col items-center">
        <div class="font-special text-special-pink text-5xl mb-4">
          Data stream
        </div>
      </div>
    <div class="flex space-x-4">
      <div class="flex flex-col items-center m-2">
        <div class="w-[640px] h-[360px] object-cover bg-black">
          <img :src="imageUrl">
        </div>
      </div>
      <div class="mt-2">
        <div class="w-[300px] bg-special-pink text-black font-bold rounded-lg p-4 mb-2 overflow-auto whitespace-normal">
          <div>Controller temperature: {{ sensorData.controller_temp }} °C</div>
          <div>Camera temperature: {{ sensorData.temp }} °C</div>
          <div>Humidity: {{ sensorData.humidity }} RH</div>
        </div>
        <div class="flex">
          <button @click="move('left')" class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-l-full">Move Left</button>
          <button @click="move('right')" class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-r-full">Move Right</button>
        </div>
        <div class="mt-2">
          <div v-if="isPlaying">
            <button @click="pauseVideo"
              class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-full">
              Pause camera stream
            </button>
          </div>
          <div v-else>
            <button @click="playVideo"
              class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-full">
              Play camera stream
            </button>
          </div>
        </div>
      </div>
    </div>
      <div class="flex flex-col items-center">
        <div class="font-special text-special-pink text-5xl mb-4">
          Search captured frames
        </div>
      </div>
    <div class="flex flex-col">
      <div class="flex items-center justify-center">
        <button @click="prevPage" class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-l-full">Previous page</button>
        <input type="number" v-model.number="page" @change="fetchImages(page)" class="bg-special-pink text-black font-bold py-1 px-4 appearance-none" min="1">
        <button @click="nextPage" class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4">Next page</button>
        <button @click="fetchImages(page)" class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-r-full">Search</button>
      </div>
      <div v-if="images.length !== 0" class="flex-shrink-0 flex overflow-x-scroll space-x-2 mx-2">
        <div v-for="(image, index) in images" :key="index" class="flex-shrink-0 flex py-2">
          <img :src="image" class="w-[640px] h-[360px]" />
        </div>
      </div>
      <div v-else class="flex flex-col items-center">
        <div class="font-special text-special-pink mb-4">
          No images loaded
        </div>
      </div>
    </div>
  </main>
  <footer class="bg-black">
    footer
  </footer>
</template>

<style scoped>
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style>
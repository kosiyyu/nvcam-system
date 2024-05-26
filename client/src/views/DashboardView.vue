<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import { ref, onMounted, onUnmounted } from "vue";
import { io } from "socket.io-client";
import { isAuthenticated } from "@/utils/authUtils";
import { Socket } from "socket.io-client";
import { isSocket } from "@/utils/dashboardUtils";

let isPlaying = ref(false);
let imageUrl = ref('');
let socket: Socket | unknown = null;

onMounted(() => {
  socket = io('http://localhost:8003');
  // socket = io('http://localhost:8003', { transports: ['websocket'] });

  if (!isSocket(socket)) {
    return;
  }

  socket.on('connect', () => {
    console.log('Connected to signaling server');
  });

  socket.on('ready', () => {
    console.log('Ready to receive frames');
  });

  socket.on('frame', (data) => {
    if (!isPlaying.value) return;
    // console.log(`Received frame of size: ${data.byteLength} bytes`);
    const uint8Array = new Uint8Array(data);
    const blob = new Blob([uint8Array], { type: 'image/jpeg' });
    imageUrl.value = URL.createObjectURL(blob);
  });

  socket.on('disconnect', () => {
    console.log('Disconnected from signaling server');
  });

  socket.on('connect_error', (error) => {
    console.error(`Connection error: ${error}`);
  });
});

onUnmounted(() => {
  if (isSocket(socket)) {
    socket.disconnect();
  }
});

function playVideo() {
  isPlaying.value = true;
}

function pauseVideo() {
  isPlaying.value = false;
}
</script>

<template>
  <NavBar :is-authenticated="isAuthenticated" />
  <main class="bg-green-950 flex flex-col items-center h-screen">
    <div>
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
    </div>
  </main>
  <footer class="bg-black">
    footer
  </footer>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { logout } from "@/utils/authUtils";
import router from "@/router";

const name = ref(localStorage.getItem("name") || "");
const isOpen = ref(false);

function register() {
  router.push({ name: "register" });
}

function login() {
  router.push({ name: "home" });
}

function chat() {
  router.push({ name: "chat" });
}

defineProps<{
  isAuthenticated: boolean
}>();
</script>

<template>
  <header class="bg-white py-2 px-1">
    <div class="flex items-center justify-between bg-white rounded-lg py-2 px-2">
      <div class="font-special text-2xl text-black">
        NVCam
      </div>
      <div class="flex items-center">
        <div v-if="!isAuthenticated" class="flex items-center">
          <button @click="login" class="bg-white h-8 hover:bg-special text-black font-bold py-1 px-4 rounded-full ml-2">
            Log in
          </button>
          <button @click="register" class="bg-white h-8 hover:bg-special text-black font-bold py-1 px-4 rounded-full ml-2">
            Register
          </button>
        </div>
        <div v-else @click="isOpen = !isOpen" class="flex items-center">
          <img alt="Vue logo" class="h-8 w-8" src="@/assets/avatars/avatar21.svg" />
          <div class="bg-white h-8 text-black font-bold py-1 px-4 rounded-full">
            {{ name }}
          </div>
          <div v-if="isOpen"
          class="flex flex-col items-center absolute top-0 right-0 mt-16 bg-white pt-2 pb-3 rounded-b-xl px-6 z-10">
            <button @click="chat" class="h-8 hover:bg-special text-black font-bold py-1 px-4 rounded-full mb-2">
              Chat
            </button>
            <button @click="register" class="h-8 hover:bg-special text-black font-bold py-1 px-4 rounded-full mb-2">
              Register
            </button>
            <button @click="logout" class="h-8 hover:bg-special text-black font-bold pt-y px-4 rounded-full mb-2">
              Log out
            </button>
          </div>

        </div>
        <!-- <div class="ml-2 h-8 w-8">
          <a href="https://github.com/kosiyyu/ai-based-microservice">
          <img src="../assets/github-mark.svg" />
          </a>
      </div> -->
      </div>
    </div>
  </header>
</template>
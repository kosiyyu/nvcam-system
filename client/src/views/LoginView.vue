<script setup lang="ts">
import { ref } from 'vue';
import router from '@/router';
import { isAuthenticated, getName } from "@/utils/authUtils";
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

const email = ref('');
const password = ref('');

function clearInputFields() {
  email.value = '';
  password.value = '';
}

const submitForm = () => {
  console.log(email.value, password.value);

  axios.post('http://localhost:5003/api/authenticate', {
    email: email.value,
    password: password.value
  }, {
    withCredentials: true
  })
  .then(response => {
    const jwt = response.data;
    if (!jwt) {
      clearInputFields();
      return;
    }
    localStorage.setItem('jwt', jwt);
    localStorage.setItem('name', getName(jwt))
    clearInputFields();
    isAuthenticated.value = true;
    console.log(isAuthenticated.value);
    router.push({ name: 'dashboard' });
  })
  .catch(error => {
    console.log(error);
  });
};
</script>

<template>
    <NavBar :is-authenticated="isAuthenticated"/>
    <main class="bg-green-950 flex flex-col items-center h-screen">
  <div class="flex flex-grow items-center justify-center flex-col">
    <div class="font-special text-special-pink text-5xl mb-4">
      Login - NVCam
    </div>
    <div class="flex items-center justify-center">
      <img src="../assets/pixeltrue-vision-1.svg" class="w-72 h-72"/>
      <div class="bg-black border border-black flex flex-col items-center justify-center p-6 inline-block rounded-tr-lg rounded-br-lg">
        <div class="m-2 flex flex-col">
          <label class="text-special-pink font-bold mb-2">Email</label>
          <input v-model="email" class="bg-special-pink  text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-special-pink"/>
        </div>
        <div class="p-2 flex flex-col">
          <label class="text-special-pink font-bold mb-2">Password</label>
          <input v-model="password" class="bg-special-pink  text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-special-pink" type="password"/>
        </div>
        <div class="flex items-center justify-center p-2">
          <button @click="submitForm" class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-full">
            Log in
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
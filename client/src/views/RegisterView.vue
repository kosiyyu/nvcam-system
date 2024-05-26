<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { isAuthenticated } from '@/utils/authUtils';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

const name = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const router = useRouter();

function clearInputFields() {
  email.value = '';
  password.value = '';
}

const submitForm = () => {
    // todo - add propper frontend validation
    if (password.value !== confirmPassword.value) {
        alert('Passwords do not match');
        return;
    }
    if(password.value.length < 8) {
        alert('Password must be at least 8 characters');
        return;
    }
    if(name.value.length < 1) {
        alert('Password must be at least 1 characters');
        return;
    }
    if(email.value.length < 2) {
        alert('Password must be at least 2 characters');
        return;
    }

  axios.post('http://localhost:5003/api/register', {
    name: name.value,
    email: email.value,
    password: password.value
  })
  .then(response => {
    console.log(response);
    clearInputFields();
    router.push({ name: 'home' });
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
      Register - NVCam
    </div>
    <div class="flex items-center justify-center">
      <img src="../assets/pixeltrue-vision-1.svg" class="w-72 h-72"/>
      <div class="bg-black border border-black flex flex-col items-center justify-center p-6 inline-block rounded-tr-lg rounded-br-lg">
        <div class="m-2 flex flex-col">
          <label class="text-special-pink font-bold mb-2">Name</label>
          <input v-model="name" class="bg-special-pink  text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-special-pink"/>
        </div>
        <div class="m-2 flex flex-col">
          <label class="text-special-pink font-bold mb-2">Email</label>
          <input v-model="email" class="bg-special-pink  text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-special-pink"/>
        </div>
        <div class="p-2 flex flex-col">
          <label class="text-special-pink font-bold mb-2">Password</label>
          <input v-model="password" class="bg-special-pink  text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-special-pink" type="password"/>
        </div>
        <div class="p-2 flex flex-col">
          <label class="text-special-pink font-bold mb-2">Confirm password</label>
          <input v-model="confirmPassword" class="bg-special-pink  text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-special-pink" type="password"/>
        </div>
        <div class="flex items-center justify-center p-2">
          <button @click="submitForm" class="bg-special-pink hover:bg-special-pink text-black font-bold py-1 px-4 rounded-full">
            Register
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
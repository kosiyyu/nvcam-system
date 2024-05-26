import { ref } from 'vue';
import { jwtDecode } from 'jwt-decode';
import router from '@/router';
import axios from 'axios';

type PartialCustomJwtPayload = {
  'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name': string;
}

function initIsAuthenticated() {
  const jwt = localStorage.getItem('jwt');
  if (jwt) {
    return true;
  }
  return false;
}

export const isAuthenticated = ref(initIsAuthenticated());

export async function checkIsAuthenticated() {
  console.log("test");
  axios.get("http://localhost:5003/api/validate", {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem("jwt")}`
    },
    withCredentials: true
  })
    .then(response => {
      if (response.status === 200) {
        isAuthenticated.value = true;
      } else {
        isAuthenticated.value = false;
        router.push({ name: 'home' });
      }
    })
    .catch(() => {
      isAuthenticated.value = false;
      router.push({ name: 'home' });
    });
}

export function getName(jwt: string): string {
  return jwtDecode<PartialCustomJwtPayload>(jwt)['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name'];
}

export function getJwt(): string {
  const jwt = localStorage.getItem('jwt');
  return jwt ? jwt : '';
}

export function logout() {
  localStorage.removeItem('jwt');
  localStorage.removeItem('name');
  isAuthenticated.value = false;
  router.push({ name: 'home' });
}
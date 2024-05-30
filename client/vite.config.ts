import { fileURLToPath, URL } from 'node:url'
import dotenv from 'dotenv';
import fs from 'fs';

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import VueDevTools from 'vite-plugin-vue-devtools'

const data = fs.readFileSync('../utils/nvcam.conf', 'utf8');
const config = dotenv.parse(data);

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    'import.meta.env.IP': JSON.stringify(config.IP),
  },
  plugins: [
    vue(),
    vueJsx(),
    VueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})

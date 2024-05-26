/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './public/**/*.html',
    './src/**/*.{js,jsx,ts,tsx,vue}',
  ],
  theme: {
    extend: {
      colors: {
        'special': 'rgba(19, 247, 46, 0.8)',
        'special-pink': 'rgba(254, 164, 211, 0.8)',
        'special-pink-2': 'rgba(254, 164, 211, 0.7)',
      },
      fontFamily: {
        'special': ['Abril Fatface', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
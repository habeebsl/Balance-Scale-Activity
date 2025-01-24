/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue, ts, js, jsx, tsx}'
  ],
  theme: {
    extend: {
      animation: {
        slideIn: 'slideIn 0.2s ease',
      },
      keyframes: {
        slideIn: {
          '0%': {
            opacity: '0',
            transform: 'translateY(-10px)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
      },
      fontFamily: {
        sans: ['Poppins', 'sans-serif']
      },
      gridTemplateColumns: {
        '70/30': '70 28%'
      },   
    },
  },
  variants: {},
  plugins: [],
}
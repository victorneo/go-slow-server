/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'valencia': {
          '50': '#fdf3f4',
          '100': '#fce4e5',
          '200': '#faced0',
          '300': '#f5acb0',
          '400': '#ed7c82',
          '500': '#de434b',
          '600': '#cd353d',
          '700': '#ac2930',
          '800': '#8e262b',
          '900': '#772529',
          '950': '#400f12',
        },
        'primary': {
          '50': '#fef2f2',
          '100': '#fee2e2',
          '200': '#fecacb',
          '300': '#fcabac', // main colour
          '400': '#f87173',
          '500': '#ef4446',
          '600': '#dc2628',
          '700': '#b91c1e',
          '800': '#991b1d',
          '900': '#7f1d1e',
          '950': '#450a0b',
        },
        'secondary': {
          '50': '#f7f4fe',
          '100': '#efebfc',
          '200': '#e3dafa',
          '300': '#cebdf5',
          '400': '#b597ee',
          '500': '#9c6de5',
          '600': '#8d4ed9',
          '700': '#7d3cc5',
          '800': '#6932a5',
          '900': '#572a88',
          '950': '#3e1d68', // main colour
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'),
  ],
}


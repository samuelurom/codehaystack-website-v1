/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./codehaystack/templates/**/*.{html,js}"],
  theme: {
    screens: {
      sm: '480px',
      md: '768px',
      lg: '976px',
      xl: '1240px'
    },
    extend: {
      maxWidth: {
        'sidebar': '300px'
      },
      minWidth: {
        'sidebar': '300px'
      }
    },
  },
  plugins: [],
}

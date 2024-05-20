/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./movies/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    ],
}


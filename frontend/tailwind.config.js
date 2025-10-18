/**
 * Tailwind CSS configuration for the Autonomy Loop frontend.
 *
 * This file tells Tailwind where to find class names and allows
 * extension of the default theme. Additional plugins can be added
 * here as needed.
 */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#4F46E5', // indigo-600
          light: '#6366F1',   // indigo-500
          dark: '#4338CA',    // indigo-700
        },
      },
    },
  },
  plugins: [],
};
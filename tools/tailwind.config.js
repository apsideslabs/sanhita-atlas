/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./dist/**/*.html"],
  theme: {
    extend: {
      colors: {
        ink: "#101a16",
        brass: "#b07d2a",
        paper: "#faf9f6"
      },
      fontFamily: {
        head: ["Sora", "ui-sans-serif", "system-ui", "sans-serif"],
        body: ["Public Sans", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"]
      }
    }
  },
  plugins: []
};

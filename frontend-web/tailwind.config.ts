import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        emergency: { DEFAULT: "#DC2626", dark: "#B91C1C", light: "#FEE2E2" },
        medical: { DEFAULT: "#0EA5E9", dark: "#0284C7" },
      },
    },
  },
  plugins: [],
};
export default config;

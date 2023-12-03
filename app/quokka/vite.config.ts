import { defineConfig } from "vite"
import { svelte } from "@sveltejs/vite-plugin-svelte"
import { VitePWA, VitePWAOptions } from "vite-plugin-pwa"

const pwaConfig: Partial<VitePWAOptions> = {
  base: "/",
  registerType: "autoUpdate",
  injectRegister: "auto",
  strategies: "generateSW",
  manifest: {
    name: "Quokka",
    short_name: "Quokka",
    description: "Génère un city-trip personnalisé en Belgique grâce à Quokka",
    theme_color: "#97d4e4",
    lang: "fr",
    background_color: "#242424",
    orientation: "landscape",
    display: "standalone",
    icons: [
      {
        src: "icons/manifest-icon-192.maskable.png",
        sizes: "192x192",
        type: "image/png",
        purpose: "any",
      },
      {
        src: "icons/manifest-icon-192.maskable.png",
        sizes: "192x192",
        type: "image/png",
        purpose: "maskable",
      },
      {
        src: "icons/manifest-icon-512.maskable.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "any",
      },
      {
        src: "icons/manifest-icon-512.maskable.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "maskable",
      },
    ],
    prefer_related_applications: false,
    shortcuts: [
      {
        name: "Ouvrir le site",
        short_name: "Ouvrir",
        description: "Ouvrir le site quokka",
        url: "/",
        icons: [
          {
            src: "icons/manifest-icon-192.maskable.png",
            sizes: "192x192",
          },
        ],
      },
    ],
    display_override: ["window-controls-overlay"],
  },
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte(), VitePWA(pwaConfig)],
  appType: "spa",
  build: {
    outDir: "../../dist/quokka",
    emptyOutDir: true,
    sourcemap: false,
    rollupOptions: {
      input: {
        main: "./index.html",
      },
    },
  },
  base: "/app/",
})

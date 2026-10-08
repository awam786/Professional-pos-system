import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),

    VitePWA({
      registerType: "autoUpdate",

      includeAssets: [
        "favicon.svg",
      ],

      manifest: {
        name: "Professional General Store POS",
        short_name: "POS",
        description:
          "Professional offline-capable General Store POS",
        theme_color: "#09090b",
        background_color: "#09090b",
        display: "standalone",
        orientation: "landscape",

        icons: [
          {
            src: "/pwa-192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "/pwa-512.png",
            sizes: "512x512",
            type: "image/png",
          },
        ],
      },

      workbox: {
        cleanupOutdatedCaches: true,

        navigateFallback:
          "/index.html",

        runtimeCaching: [
          {
            urlPattern:
              /^https:\/\/fonts\.(googleapis|gstatic)\.com\/.*/i,

            handler: "CacheFirst",

            options: {
              cacheName: "google-fonts",
              expiration: {
                maxEntries: 20,
                maxAgeSeconds:
                  60 * 60 * 24 * 365,
              },
            },
          },
        ],
      },
    }),
  ],

  server: {
    host: "0.0.0.0",
    port: 5173,
  },

  build: {
    target: "es2022",
    sourcemap: false,
  },
});

import { defineConfig } from "@lovable.dev/vite-tanstack-config";

export default defineConfig({
  nitro: true, // Enable Nitro
  tanstackStart: {
    server: { entry: "server" },
  },
});

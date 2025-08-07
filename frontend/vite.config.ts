import tailwindcss from "@tailwindcss/vite";
import react from '@vitejs/plugin-react';
import path from 'node:path';
import { defineConfig } from 'vite';
import { viteStaticCopy } from 'vite-plugin-static-copy';

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    viteStaticCopy({
      targets: [
        {
          src: path.resolve(__dirname, './WebSDK/Core/live2dcubismcore.js'),
          dest: './libs/',
        },
      ],
    }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@framework": path.resolve(__dirname, "./WebSDK/Framework/src"),
      "@cubismsdksamples": path.resolve(__dirname, "./WebSDK/src"),
      "@motionsyncframework": path.resolve(
        __dirname,
        "./MotionSync/Framework/src",
      ),
      "@motionsync": path.resolve(__dirname, "./MotionSync/src"),
    },
  },
})

import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  plugins: [sveltekit()],
  resolve: {
    alias: {
      // Tohle je to nejdůležitější – díky tomu Vite najde three/addons
      'three/addons': path.resolve('node_modules/three/examples/jsm')
    }
  },
  optimizeDeps: {
    include: ['three']
  }
});
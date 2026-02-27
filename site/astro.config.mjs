import { defineConfig } from 'astro/config';

export default defineConfig({
  outDir: './dist',
  publicDir: './public',
  build: {
    assets: '_astro'
  }
});

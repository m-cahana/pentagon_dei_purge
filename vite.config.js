import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    sveltekit({
      compilerOptions: {
        // Enable the Svelte 5 compiler
        generate: "dom",
        hydratable: true,
      },
    }),
  ],
  optimizeDeps: {
    exclude: ["chunk-VAYVOWOY", "chunk-V32KMRUZ"],
  },
});

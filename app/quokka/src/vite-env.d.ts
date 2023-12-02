/// <reference types="svelte" />
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BASE_URL_API: string
  // more env variables...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

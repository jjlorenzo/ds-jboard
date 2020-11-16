declare function fetch(input: Request | string | URL, init?: RequestInit): Promise<Response>

declare module "*.gif" {
  const src: string
  export default src
}

declare module "*.jpeg" {
  const src: string
  export default src
}

declare module "*.jpg" {
  const src: string
  export default src
}

declare module "*.module.css" {
  const classes: { readonly [key: string]: string }
  export default classes
}

declare module "*.module.sass" {
  const classes: { readonly [key: string]: string }
  export default classes
}

declare module "*.module.scss" {
  const classes: { readonly [key: string]: string }
  export default classes
}

declare module "*.png" {
  const src: string
  export default src
}

declare module "*.svg" {
  const src: string
  export default src
}

declare module "*.vue" {
  import { Component } from "vue"
  const _default: Component
  export default _default
}

declare module "*.webp" {
  const src: string
  export default src
}

declare namespace NodeJS {
  interface Process {
    env: ProcessEnv
  }
  interface ProcessEnv {
    readonly NODE_ENV: "development" | "production"
  }
}

declare var process: NodeJS.Process

interface URLSearchParams {
  append(name: string, value: string | number): void
}

interface ButtonHTMLAttributes {
  busy?: boolean
}

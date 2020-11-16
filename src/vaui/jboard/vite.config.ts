const VITE_HMR_PORT = parseInt(process.env.VITE_HMR_PORT)

export default {
  hmr: {
    port: VITE_HMR_PORT,
  },
  proxy: ["conn", "djrf"].reduce((memo, name) => {
    memo[`/${name}`] = {
      target: `http://bck-${name}:8000`,
      changeOrigin: true,
      rewrite: (path: string) => path.replace(new RegExp(`/${name}`, "g"), ""),
    }
    return memo
  }, {}),
  rollupInputOptions: {
    external: ["jquery"],
  },
  vueCompilerOptions: {
    isCustomElement: (tag: string) => {
      return /^aui-/.test(tag)
    },
  },
}

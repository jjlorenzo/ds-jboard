import "@atlassian/aui/dist/aui/aui-prototyping.css"

import App from "./app.vue"
import VAuiButton from "./components/v-aui-button.vue"
import VAuiSelect from "./components/v-aui-select.vue"
import { createApp } from "vue"
import { router } from "./router"
import { store, key } from "./store"

const app = createApp(App)

app.component("v-aui-button", VAuiButton)
app.component("v-aui-select", VAuiSelect)

app.use(router)

app.use(store, key)

app.mount("#app")

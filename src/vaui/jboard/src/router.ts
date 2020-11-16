import Detail from "./pages/detail.vue"
import List from "./pages/list.vue"
import { createRouter } from "vue-router"
import { createWebHistory } from "vue-router"

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "",
      name: "list",
      component: List,
    },
    {
      path: "/:pk",
      name: "detail",
      component: Detail,
      props: true,
    },
  ],
})

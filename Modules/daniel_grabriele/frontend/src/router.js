import { createMemoryHistory, createRouter } from 'vue-router'

import DashboardPackages from '@/components/DashboardPackages.vue'

const routes = [
  { path: '/', component: DashboardPackages },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router;
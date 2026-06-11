import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: () => import('../pages/LoginPage.vue') },
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', component: () => import('../pages/DashboardPage.vue'), meta: { requiresAuth: true } },
    { path: '/accounts', component: () => import('../pages/AccountsPage.vue'), meta: { requiresAuth: true } },
    { path: '/categories', component: () => import('../pages/CategoriesPage.vue'), meta: { requiresAuth: true } },
    { path: '/transactions', component: () => import('../pages/TransactionsPage.vue'), meta: { requiresAuth: true } },
    { path: '/recurring', component: () => import('../pages/RecurringPage.vue'), meta: { requiresAuth: true } },
    { path: '/budgets', component: () => import('../pages/BudgetsPage.vue'), meta: { requiresAuth: true } },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !localStorage.getItem('finance_token')) {
    return '/login'
  }
})

export default router

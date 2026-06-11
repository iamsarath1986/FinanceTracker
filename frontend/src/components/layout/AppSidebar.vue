<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

defineProps<{ isOpen: boolean }>()
const emit = defineEmits<{ close: [] }>()

const router = useRouter()
const auth = useAuthStore()

const navItems = [
  { label: 'Dashboard', icon: 'pi pi-home', to: '/dashboard' },
  { label: 'Accounts', icon: 'pi pi-wallet', to: '/accounts' },
  { label: 'Categories', icon: 'pi pi-tags', to: '/categories' },
  { label: 'Transactions', icon: 'pi pi-list', to: '/transactions' },
  { label: 'Recurring', icon: 'pi pi-refresh', to: '/recurring' },
  { label: 'Budgets', icon: 'pi pi-chart-bar', to: '/budgets' },
]

function logout() {
  auth.logout()
  router.push('/login')
}

function navigate() {
  emit('close')
}
</script>

<template>
  <div
    class="flex flex-col h-full w-56 bg-surface-900 text-white shrink-0
           fixed md:relative z-40 transition-transform duration-300
           md:translate-x-0"
    :class="isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'"
  >
    <div class="p-4 text-xl font-bold border-b border-surface-700 flex items-center gap-2">
      <i class="pi pi-chart-pie" />FinanceTracker
    </div>
    <nav class="flex-1 p-2 overflow-y-auto">
      <RouterLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 px-3 py-2 rounded-lg mb-1 text-surface-200 hover:bg-surface-700 transition-colors"
        active-class="bg-primary-600 text-white"
        @click="navigate"
      >
        <i :class="item.icon" />
        {{ item.label }}
      </RouterLink>
    </nav>
    <div class="p-2 border-t border-surface-700">
      <button
        class="flex items-center gap-3 px-3 py-2 w-full rounded-lg text-surface-300 hover:bg-surface-700 transition-colors"
        @click="logout"
      >
        <i class="pi pi-sign-out" /> Logout
      </button>
    </div>
  </div>
</template>

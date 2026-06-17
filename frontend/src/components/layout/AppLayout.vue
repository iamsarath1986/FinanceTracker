<script setup lang="ts">
import { ref } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppTopbar from './AppTopbar.vue'

defineProps<{ title: string }>()
const sidebarOpen = ref(false)
</script>

<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-black/50 z-30 md:hidden"
      @click="sidebarOpen = false"
    />

    <AppSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />

    <div class="flex flex-col flex-1 overflow-hidden min-w-0">
      <AppTopbar :title="title" @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      <main class="flex-1 overflow-auto p-4 md:p-6 bg-surface-50">
        <slot />
      </main>
    </div>
  </div>
</template>

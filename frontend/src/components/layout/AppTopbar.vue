<script setup lang="ts">
defineProps<{ title: string }>()
defineEmits<{ toggleSidebar: [] }>()
</script>

<template>
  <header class="flex items-center h-14 px-4 md:px-6 border-b border-surface-200 bg-surface-0 shrink-0 gap-3">
    <button
      class="md:hidden p-2 rounded-lg text-surface-600 hover:bg-surface-100 transition-colors"
      @click="$emit('toggleSidebar')"
    >
      <i class="pi pi-bars text-lg" />
    </button>
    <h1 class="text-lg md:text-xl font-semibold text-surface-800">{{ title }}</h1>
  </header>
</template>

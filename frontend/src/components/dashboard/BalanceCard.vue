<script setup lang="ts">
import Card from 'primevue/card'

const props = defineProps<{ name: string; currency: string; current_balance: number }>()

function fmt(amount: number, currency: string) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(amount)
}
</script>

<template>
  <Card class="flex-1 min-w-40">
    <template #title>{{ name }}</template>
    <template #content>
      <p class="text-2xl font-bold" :class="current_balance >= 0 ? 'text-green-600' : 'text-red-600'">
        {{ fmt(current_balance, currency) }}
      </p>
      <p class="text-sm text-surface-500 mt-1">{{ currency }}</p>
    </template>
  </Card>
</template>

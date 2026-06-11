<script setup lang="ts">
import ProgressBar from 'primevue/progressbar'

defineProps<{
  items: { name: string; limit_amount: number; spent: number; currency: string }[]
}>()

function pct(spent: number, limit: number) {
  return Math.min(Math.round((spent / limit) * 100), 100)
}

function fmt(amount: number) {
  return amount.toFixed(2)
}
</script>

<template>
  <div class="flex flex-col gap-4">
    <div v-for="item in items" :key="item.name">
      <div class="flex justify-between text-sm mb-1">
        <span class="font-medium">{{ item.name }}</span>
        <span class="text-surface-500">{{ fmt(item.spent) }} / {{ fmt(item.limit_amount) }} {{ item.currency }}</span>
      </div>
      <ProgressBar :value="pct(item.spent, item.limit_amount)" :show-value="false" class="h-2" />
    </div>
    <p v-if="!items.length" class="text-surface-400 text-sm">No budgets configured.</p>
  </div>
</template>
